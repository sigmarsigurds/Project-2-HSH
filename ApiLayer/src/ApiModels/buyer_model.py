from typing import Optional
from pydantic import BaseModel
from pydantic.fields import Field


class BuyerModel(BaseModel):
    buyerId: Optional[int]
    name: str
    ssn: str
    email: str
    phoneNumber: str
