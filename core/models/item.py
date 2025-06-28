from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, relationship

from core.models.base import Base


if TYPE_CHECKING:
    from core.models import Order
    from .order_product_association import OrderProductAssociation


class Item(Base):
    __tablename__ = 'items'

    name: Mapped[str]
    description: Mapped[str]
    price: Mapped[int]
    orders: Mapped[list['Order']] = relationship(secondary='order_product_association', back_populates='products')
    orders_details: Mapped[list['OrderProductAssociation']] = relationship(back_populates='product')
