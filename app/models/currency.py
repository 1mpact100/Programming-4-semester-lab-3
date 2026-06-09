from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base

class Currency(Base):
    __tablename__ = "currencies"
    
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )
    
    code: Mapped[str] = mapped_column(
        String,
        unique=True,
        nullable=False
    )
    
    name: Mapped[str] = mapped_column(
        String,
        nullable=False
    )
