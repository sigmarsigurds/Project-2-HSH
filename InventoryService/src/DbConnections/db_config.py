from pydantic import BaseModel


class DbConfig(BaseModel):
    host: str
    database: str
    user: str
    password: str
