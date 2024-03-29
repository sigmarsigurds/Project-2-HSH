from enum import Enum
from pydantic import (BaseSettings)


class ContainerSettingEnum(Enum):
    def get(self, *argv):
        return self.value


class Environment(ContainerSettingEnum):
    DEV = 'dev'
    STAGING = 'staging'
    PROD = 'prod'


class Settings(BaseSettings):
    postgres_host: str
    postgres_database: str
    postgres_user: str
    postgres_password: str

    rabbitmq_server_host: str

    environment: Environment

    class Config:
        # env_prefix = 'INVENTORY_SERVICE_'  # defaults to no prefix, i.e. ""
        fields = {
            'postgres_host': {
                'env': 'POSTGRES_HOST',
            },
            'postgres_database': {
                'env': 'POSTGRES_DATABASE',
            },
            'postgres_user': {
                'env': 'POSTGRES_USER',
            },
            'postgres_password': {
                'env': 'POSTGRES_PASSWORD',
            },
            'rabbitmq_server_host': {
                'env': 'RABBITMQ_SERVER_HOST'
            },
            'environment': {
                'env': 'ENVIRONMENT'
            }
        }

