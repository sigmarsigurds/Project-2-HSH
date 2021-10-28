from dependency_injector import containers, providers

# from settings import Settings

from buyer_repository import BuyerRepository
from db_connections.db_config import DbConfig
from db_connections.postgres_db_connection import PostgresDbConnection


class Container(containers.DeclarativeContainer):
    # config: settings.Settings = providers.Configuration()

    __db_config = providers.Singleton(
        DbConfig,
        host="buyer_db",
        user="postgres",
        database="Buyer",
        password="password",
    )

    db_connection = providers.Singleton(
        providers.Singleton(PostgresDbConnection, __db_config)
    )
    buyer_repository_provider = providers.Singleton(
        BuyerRepository, connection=db_connection
    )
