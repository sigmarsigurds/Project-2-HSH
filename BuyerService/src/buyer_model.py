from pydantic import BaseModel


class BuyerModel(BaseModel):
    name: str
    ssn: str
    email: str
    phonenumber: str
