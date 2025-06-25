from pydantic import BaseModel


class ItemBase(BaseModel):
    name: str
    description: str
    price: int

class ItemCreate(ItemBase):
    pass

class ItemUpdate(ItemBase):
    pass

class ItemUpdatePartial(ItemBase):
    pass

class Item(ItemBase):
    id: int



