from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.currency import Currency
from app.models.subscription import Subscription
from app.models.user import User
from app.schemas.subscription import SubscriptionRequest

async def create_subscription(
    db: AsyncSession,
    subscription_data: SubscriptionRequest
) -> Subscription:
    currency = await _get_currency(db, subscription_data)
    await _ensure_user_exists(db, subscription_data.user_id)
    
    result = await db.execute(
        select(Subscription).where(
            Subscription.user_id == subscription_data.user_id,
            Subscription.currency_id == currency.id
        )
    )
    existing_subscription = result.scalar_one_or_none()
    
    if existing_subscription:
        raise HTTPException(
            status_code=409,
            detail="Subscription already exists"
        )
    
    subscription = Subscription(
        user_id=subscription_data.user_id,
        currency_id=currency.id
    )
    
    db.add(subscription)
    try:
        await db.commit()
    except IntegrityError as exc:
        await db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Subscription already exists"
        ) from exc
    
    return subscription

async def delete_subscription(
    db: AsyncSession,
    subscription_data: SubscriptionRequest
) -> dict[str, str]:
    currency = await _get_currency(db, subscription_data)
    await _ensure_user_exists(db, subscription_data.user_id)
    
    result = await db.execute(
        select(Subscription).where(
            Subscription.user_id == subscription_data.user_id,
            Subscription.currency_id == currency.id
        )
    )
    subscription = result.scalar_one_or_none()
    
    if not subscription:
        raise HTTPException(
            status_code=404,
            detail="Subscription not found"
        )
    
    await db.delete(subscription)
    await db.commit()
    
    return {"detail": "Subscription deleted"}

async def _ensure_user_exists(db: AsyncSession, user_id: int) -> None:
    user = await db.get(User, user_id)
    
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

async def _get_currency(
    db: AsyncSession,
    subscription_data: SubscriptionRequest
) -> Currency:
    if subscription_data.currency_id is not None:
        currency = await db.get(Currency, subscription_data.currency_id)
    else:
        result = await db.execute(
            select(Currency).where(
                Currency.code == subscription_data.currency_code.upper()
            )
        )
        currency = result.scalar_one_or_none()
    
    if not currency:
        raise HTTPException(
            status_code=404,
            detail="Currency not found"
        )
    
    return currency
