from pydantic import BaseModel


class ItemModel(BaseModel):
    item_id: int
    name: str
    qty: int
