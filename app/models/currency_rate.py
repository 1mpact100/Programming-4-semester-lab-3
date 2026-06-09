from datetime import date

from sqlalchemy import Date, Float, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base

class CurrencyRate(Base):
    __tablename__ = "currency_rates"
    __table_args__ = (
        UniqueConstraint("currency_id", "date"),
    )
    
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )
    
    currency_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("currencies.id", ondelete="CASCADE"),
        nullable=False
    )
    
    date: Mapped[date] = mapped_column(
        Date,
        nullable=False
    )
    
    rate: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )
