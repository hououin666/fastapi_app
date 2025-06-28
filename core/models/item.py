from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, relationship

from core.models.base import Base
from core.models.order_product_association import order_product_association_table


if TYPE_CHECKING:
    from core.models import Order


class Item(Base):
    __tablename__ = 'items'

    name: Mapped[str]
    description: Mapped[str]
    price: Mapped[int]
    orders: Mapped[list['Order']] = relationship(secondary=order_product_association_table, back_populates='items')
