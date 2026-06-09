from datetime import datetime
from xml.etree import ElementTree

import httpx
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.config import CBR_DAILY_URL
from app.models.currency import Currency
from app.models.currency_rate import CurrencyRate
from app.schemas.currency import CurrencyRateRead

async def get_currencies(db: AsyncSession) -> list[Currency]:
    result = await db.execute(select(Currency).order_by(Currency.code))
    return list(result.scalars().all())

async def update_currencies(db: AsyncSession) -> tuple[int, int]:
    try:
        async with httpx.AsyncClient(timeout=15.0, follow_redirects=True) as client:
            response = await client.get(CBR_DAILY_URL)
            response.raise_for_status()
    except httpx.HTTPError as exc:
        raise HTTPException(
            status_code=502,
            detail="Failed to fetch currencies from CBR"
        ) from exc
    
    try:
        root = ElementTree.fromstring(response.content)
        rate_date = datetime.strptime(root.attrib["Date"], "%d.%m.%Y").date()
    except (ElementTree.ParseError, KeyError, ValueError) as exc:
        raise HTTPException(
            status_code=502,
            detail="Invalid XML response from CBR"
        ) from exc
    
    updated_currencies = 0
    updated_rates = 0
    
    for item in root.findall("Valute"):
        code = item.findtext("CharCode")
        name = item.findtext("Name")
        nominal_text = item.findtext("Nominal")
        value_text = item.findtext("Value")
        
        if not code or not name or not nominal_text or not value_text:
            continue
        
        try:
            nominal = int(nominal_text)
            value = float(value_text.replace(",", "."))
        except ValueError:
            continue

        if nominal <= 0:
            continue

        rate = value / nominal
        
        currency = await _get_currency_by_code(db, code)
        
        if currency:
            currency.name = name
        else:
            currency = Currency(
                code=code,
                name=name
            )
            db.add(currency)
            await db.flush()
        
        updated_currencies += 1
        
        rate_result = await db.execute(
            select(CurrencyRate).where(
                CurrencyRate.currency_id == currency.id,
                CurrencyRate.date == rate_date
            )
        )
        currency_rate = rate_result.scalar_one_or_none()
        
        if currency_rate:
            currency_rate.rate = rate
        else:
            currency_rate = CurrencyRate(
                currency_id=currency.id,
                date=rate_date,
                rate=rate
            )
            db.add(currency_rate)
        
        updated_rates += 1
    
    await db.commit()
    
    return updated_currencies, updated_rates

async def get_latest_currency_rate(db: AsyncSession, currency_code: str) -> CurrencyRateRead:
    currency = await _get_currency_by_code(db, currency_code.upper())
    
    if not currency:
        raise HTTPException(
            status_code=404,
            detail="Currency not found"
        )
    
    result = await db.execute(
        select(CurrencyRate)
        .where(CurrencyRate.currency_id == currency.id)
        .order_by(CurrencyRate.date.desc(), CurrencyRate.id.desc())
        .limit(1)
    )
    currency_rate = result.scalar_one_or_none()
    
    if not currency_rate:
        raise HTTPException(
            status_code=404,
            detail="Currency rate not found"
        )
    
    return CurrencyRateRead(
        currency_code=currency.code,
        currency_name=currency.name,
        date=currency_rate.date,
        rate=currency_rate.rate
    )

async def _get_currency_by_code(db: AsyncSession, currency_code: str) -> Currency | None:
    result = await db.execute(
        select(Currency).where(Currency.code == currency_code.upper())
    )
    return result.scalar_one_or_none()
