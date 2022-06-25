from pydantic import BaseModel
from typing import Union


class Item(BaseModel):
    task : str
    rating:int

