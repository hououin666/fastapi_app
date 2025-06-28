from typing import Optional, Annotated

from pydantic import BaseModel
from sqlalchemy.orm import mapped_column

from api_v1.users.schemas import User


class PostBase(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    bio: Optional[str]
    user_id: Annotated[int]
    user: Annotated[User]

