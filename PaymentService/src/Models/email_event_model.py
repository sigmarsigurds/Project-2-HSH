from pydantic import BaseModel
from pydantic.fields import Field


class EmailEventModel(BaseModel):
    email_to: str
    subject: str
    content: str
