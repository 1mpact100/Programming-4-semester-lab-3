from app.core.database import AsyncSessionLocal
from sqlalchemy.ext.asyncio import AsyncSession
from collections.abc import AsyncGenerator

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session