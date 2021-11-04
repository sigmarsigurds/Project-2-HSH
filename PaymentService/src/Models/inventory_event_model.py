from pydantic import BaseModel
from pydantic.fields import Field


class InventoryEventModel(BaseModel):
    product_id: int = Field(..., alias="productId")
    quantity: int = 1
