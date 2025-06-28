from sqlalchemy import Table, Integer, Column, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from core.models import Base

# order_product_association_table = Table(
#     'order_product_association',
#     Base.metadata,
#     Column('id', Integer, primary_key=True),
#     Column('order_id', ForeignKey('orders.id'), nullable=False),
#     Column('item_id', ForeignKey('items.id'), nullable=False),
#     UniqueConstraint('order_id', 'item_id', name='idx_unique_order_product')
# )


class OrderProductAssociation(Base):
    __tablename__ = 'order_product_association'
    __table_args__ = (
        UniqueConstraint(
            'order_id',
            'item_id',
            name='idx_unique_order_product'
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey('orders.id'))
    item_id: Mapped[int] = mapped_column(ForeignKey('items.id'))