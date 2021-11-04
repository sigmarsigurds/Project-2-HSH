from typing import Optional
from pydantic import BaseModel


class TransactionModel(BaseModel):
    id: Optional[int] = None
    order_id: int
    success: bool = False

