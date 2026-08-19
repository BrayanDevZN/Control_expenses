"""
Model de expanses
"""

from pydantic import BaseModel

class validExpanse(BaseModel):

    public_id: int|str
    name: str
    quantity: int
    price:float