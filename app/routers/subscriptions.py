from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.database import get_db
from app.schemas.subscription import SubscriptionRead, SubscriptionRequest
from app.services.subscription import create_subscription, delete_subscription

router = APIRouter(prefix="/subscriptions", tags=["subscriptions"])

@router.post("/", response_model=SubscriptionRead, status_code=status.HTTP_201_CREATED)
async def subscribe_to_currency(
    subscription_data: SubscriptionRequest,
    db: AsyncSession = Depends(get_db)
):
    return await create_subscription(db, subscription_data)

@router.delete("/")
async def unsubscribe_from_currency(
    subscription_data: SubscriptionRequest,
    db: AsyncSession = Depends(get_db)
):
    return await delete_subscription(db, subscription_data)
