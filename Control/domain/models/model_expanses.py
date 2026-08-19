"""
Model de expanses
"""

from pydantic import BaseModel, Field, field_validator
from typing import Literal
class validExpanse(BaseModel):

    public_id: int|str
    name: str
    quantity: int = Field(gt=0)
    price:float = Field(gt=0)


class ValidUpdateExpanses(BaseModel):
    name:str
    set:Literal["name", "quantity", "price"]
    value:str|float|int


    #Se value for um int ou float, valida se é maior que zero
    @field_validator("value")
    def valid(cls, v):

        if isinstance(v, int) or isinstance(v, float):

            if v <= 0:

                raise ValueError("The value is less than zero")


        return v

