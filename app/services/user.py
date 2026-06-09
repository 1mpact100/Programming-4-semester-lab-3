from fastapi import HTTPException
from sqlalchemy import delete, or_, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.currency import Currency
from app.models.subscription import Subscription
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate, UserWithSubscriptions

async def get_users(db: AsyncSession) -> list[User]:
    result = await db.execute(select(User))
    return list(result.scalars().all())

async def get_user(db: AsyncSession, user_id: int) -> UserWithSubscriptions:
    user = await _get_user_or_404(db, user_id)
    
    result = await db.execute(
        select(Currency)
        .join(Subscription, Subscription.currency_id == Currency.id)
        .where(Subscription.user_id == user.id)
        .order_by(Currency.code)
    )
    currencies = list(result.scalars().all())
    
    return UserWithSubscriptions(
        id=user.id,
        username=user.username,
        email=user.email,
        subscriptions=currencies
    )

async def create_user(db: AsyncSession, user_data: UserCreate) -> User:
    result = await db.execute(
        select(User).where(
            or_(
                User.username == user_data.username,
                User.email == user_data.email
            )
        )
    )
    existing_user = result.scalar_one_or_none()
    
    if existing_user:
        raise HTTPException(
            status_code=409,
            detail="User with this username or email already exists"
        )
    
    user = User(
        username=user_data.username,
        email=user_data.email
    )
    
    db.add(user)
    try:
        await db.commit()
    except IntegrityError as exc:
        await db.rollback()
        raise HTTPException(
            status_code=409,
            detail="User with this username or email already exists"
        ) from exc
    await db.refresh(user)
    
    return user

async def update_user(
    db: AsyncSession,
    user_id: int,
    user_data: UserUpdate
) -> User:
    user = await _get_user_or_404(db, user_id)
    update_data = user_data.model_dump(exclude_unset=True, exclude_none=True)
    
    if not update_data:
        return user
    
    result = await db.execute(
        select(User).where(
            User.id != user_id,
            or_(
                User.username == update_data.get("username"),
                User.email == update_data.get("email")
            )
        )
    )
    existing_user = result.scalar_one_or_none()
    
    if existing_user:
        raise HTTPException(
            status_code=409,
            detail="User with this username or email already exists"
        )
    
    for field, value in update_data.items():
        setattr(user, field, value)
    
    try:
        await db.commit()
    except IntegrityError as exc:
        await db.rollback()
        raise HTTPException(
            status_code=409,
            detail="User with this username or email already exists"
        ) from exc
    await db.refresh(user)
    
    return user

async def delete_user(db: AsyncSession, user_id: int) -> dict[str, str]:
    user = await _get_user_or_404(db, user_id)
    
    await db.execute(
        delete(Subscription).where(Subscription.user_id == user_id)
    )
    await db.delete(user)
    await db.commit()
    
    return {"detail": "User deleted"}

async def _get_user_or_404(db: AsyncSession, user_id: int) -> User:
    user = await db.get(User, user_id)
    
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    
    return user
