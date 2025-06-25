from sqlalchemy.orm import Mapped

from core.models.base import Base


class Item(Base):
    __tablename__ = 'items'

    name: Mapped[str]
    description: Mapped[str]
    price: Mapped[int]

