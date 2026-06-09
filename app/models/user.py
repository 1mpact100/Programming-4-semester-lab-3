from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base

class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )
    
    username: Mapped[str] = mapped_column(
        String,
        unique=True,
        nullable=False
    )
    
    email: Mapped[str] = mapped_column(
        String,
        unique=True,
        nullable=False
    )