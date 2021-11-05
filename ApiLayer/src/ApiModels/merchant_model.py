from typing import Optional
from pydantic import BaseModel, Field


class MerchantModel(BaseModel):
    name: str
    ssn: str
    email: str
    phoneNumber: str
    allowsDiscount: bool


