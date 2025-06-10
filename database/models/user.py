from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from .base import Base
from sqlalchemy import String,BigInteger

class User(Base):
    __tablename__='users'

    id:Mapped[int]=mapped_column(BigInteger,primary_key=True)#tg_id
    name:Mapped[str]=mapped_column(String(60))
    email:Mapped[str]=mapped_column(String(125))
    phone_number:Mapped[str]=mapped_column(String(20))
