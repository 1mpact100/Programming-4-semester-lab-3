from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base

class Subscription(Base):
    __tablename__ = "subscriptions"
    
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True
    )
    
    currency_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("currencies.id", ondelete="CASCADE"),
        primary_key=True
    )
