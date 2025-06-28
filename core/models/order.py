from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models import Base, Item
from core.models.order_product_association import order_product_association_table

if TYPE_CHECKING:
    from core.models import Item

class Order(Base):
    __tablename__ = 'orders'

    promocode: Mapped[str | None]
    created_at: Mapped[datetime] = mapped_column(server_default=func.now(), default=datetime.utcnow)
    products: Mapped[list['Item']] = relationship(secondary=order_product_association_table, back_populates='orders')

