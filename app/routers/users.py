from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.database import get_db
from app.schemas.user import UserCreate, UserRead, UserUpdate, UserWithSubscriptions
from app.services.user import create_user, delete_user, get_user, get_users, update_user

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/", response_model=list[UserRead])
async def get_all_users(db: AsyncSession = Depends(get_db)):
    return await get_users(db)

@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def create_new_user(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    return await create_user(db, user_data)

@router.get("/{user_id}", response_model=UserWithSubscriptions)
async def get_user_by_id(
    user_id: int,
    db: AsyncSession = Depends(get_db)
):
    return await get_user(db, user_id)

@router.put("/{user_id}", response_model=UserRead)
async def update_user_by_id(
    user_id: int,
    user_data: UserUpdate,
    db: AsyncSession = Depends(get_db)
):
    return await update_user(db, user_id, user_data)

@router.delete("/{user_id}")
async def delete_user_by_id(
    user_id: int,
    db: AsyncSession = Depends(get_db)
):
    return await delete_user(db, user_id)
