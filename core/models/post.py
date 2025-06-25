from enum import unique

from sqlalchemy import String, Text, ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.testing.schema import mapped_column

from core.models import Base


class Post(Base):
    __tablename__ = 'posts'

    title: Mapped[str] = mapped_column(String(100), unique=False)
    body: Mapped[str] = mapped_column(Text, default='', server_default='')
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))

