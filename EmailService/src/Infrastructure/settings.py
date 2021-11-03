from enum import Enum
from pydantic import BaseSettings


class ContainerSettingEnum(Enum):
    def get(self, *argv):
        return self.value


class Environment(ContainerSettingEnum):
    DEV = "dev"
    STAGING = "staging"
    PROD = "prod"


class Settings(BaseSettings):
    host: str
    port: int

    email: str
    password: str

    environment: Environment

    class Config:
        fields = {
            "host": {"env": "HOST"},
            "port": {"PORT": "PORT"},
            "postgres_host": {
                "env": "POSTGRES_HOST",
            },
            "postgres_database": {
                "env": "POSTGRES_DATABASE",
            },
            "postgres_user": {
                "env": "POSTGRES_USER",
            },
            "postgres_password": {
                "env": "POSTGRES_PASSWORD",
            },
            "environment": {"env": "ENVIRONMENT"},
        }
