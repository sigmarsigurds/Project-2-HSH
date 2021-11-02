from pydantic import BaseModel


class ApiReserveProductModel(BaseModel):
    quantity: int
