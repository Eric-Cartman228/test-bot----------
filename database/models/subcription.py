from sqlalchemy import ForeignKey, Boolean, Column, Integer, Date, func
from sqlalchemy.orm import Mapped, relationship, mapped_column
from .base import Base
from sqlalchemy import String, BigInteger, ARRAY


class Subcription(Base):
    __tablename__ = "subscriptions"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(String(60))
    description: Mapped[str] = mapped_column(String(120))
    channel_id: Mapped[list[str]] = mapped_column(ARRAY(String))
    status: Mapped[bool] = mapped_column(Boolean, nullable=True, default=True)
    subscriptions = relationship("UserSubcriptions", back_populates="subscription")
