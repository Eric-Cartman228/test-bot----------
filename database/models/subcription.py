from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from .base import Base
from sqlalchemy import String, BigInteger


class Subcription(Base):
    __tablename__ = "Subscriptions"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(String(60))
    description: Mapped[str] = mapped_column(String(120))
