from sqlalchemy import ForeignKey, Boolean, Column, Integer, Date, func
from sqlalchemy.orm import Mapped, relationship, mapped_column
from .base import Base
from sqlalchemy import String, BigInteger, ARRAY


class UserSubcriptions(Base):
    __tablename__ = "user_subsscription"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    user_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("users.id"), nullable=True
    )
    subscription_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("subscriptions.id"), nullable=True
    )
    date_activate: Mapped[Date] = mapped_column(Date, nullable=True)
    date_expired: Mapped[Date] = mapped_column(Date, nullable=True)
    ended_sub: Mapped[bool] = mapped_column(Boolean, default=False)
    extend_subs: Mapped[bool] = mapped_column(Boolean, default=False)

    user = relationship("User", back_populates="subscriptions")
    subscription = relationship("Subcription", back_populates="subscriptions")
