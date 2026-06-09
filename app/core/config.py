import os


DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./app.db")
CBR_DAILY_URL = os.getenv(
    "CBR_DAILY_URL",
    "https://www.cbr.ru/scripts/XML_daily.asp",
)
