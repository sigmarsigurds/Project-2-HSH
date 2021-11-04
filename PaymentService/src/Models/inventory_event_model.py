from pydantic import BaseModel


class InventoryEventModel(BaseModel):
    product_id: int
    quantity: int = 1
