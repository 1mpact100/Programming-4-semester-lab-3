from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.database import get_db
from app.schemas.currency import CurrenciesUpdateResult, CurrencyRateRead, CurrencyRead
from app.services.currency import get_currencies, get_latest_currency_rate, update_currencies

router = APIRouter(prefix="/currencies", tags=["currencies"])

@router.get("/", response_model=list[CurrencyRead])
async def get_all_currencies(db: AsyncSession = Depends(get_db)):
    return await get_currencies(db)

@router.post("/update", response_model=CurrenciesUpdateResult)
async def update_all_currencies(db: AsyncSession = Depends(get_db)):
    updated_currencies, updated_rates = await update_currencies(db)
    
    return CurrenciesUpdateResult(
        updated_currencies=updated_currencies,
        updated_rates=updated_rates
    )

@router.get("/{currency_code}/rate", response_model=CurrencyRateRead)
async def get_currency_rate(
    currency_code: str,
    db: AsyncSession = Depends(get_db)
):
    return await get_latest_currency_rate(db, currency_code)
