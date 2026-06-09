from fastapi import FastAPI
from app.core.database import engine, Base
from contextlib import asynccontextmanager
from app.routers import router
from app.models.user import User
from app.models.currency import Currency
from app.models.currency_rate import CurrencyRate
from app.models.subscription import Subscription

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
            
    yield

app = FastAPI(
    title="Currency Tracker API",
    description="REST API для пользователей, подписок и курсов валют ЦБ РФ",
    version="1.0.0",
    lifespan=lifespan,
)
app.include_router(router)
