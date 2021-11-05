from typing import Optional
from pydantic import BaseModel, Field
from decimal import Decimal


class ProductModel(BaseModel):
    merchantId: int
    name: str
    price: Decimal
    quantity: int
    reserved: int = 0  # * When a post request is done, number of reserved units are not provide
