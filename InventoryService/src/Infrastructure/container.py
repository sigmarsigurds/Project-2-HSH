from dependency_injector import containers, providers

from src.Repositories import InventoryRepository
from src.DbConnections import DbConfig, PostgresDbConnection
import src.Infrastructure.settings as settings
from src.Models import ServiceModel


class Container(containers.DeclarativeContainer):
    config: settings.Settings = providers.Configuration()

    __db_config = providers.Singleton(
        DbConfig,
        host=config.postgres_host,
        user=config.postgres_user,
        database=config.postgres_database,
        password=config.postgres_password
    )

    merchant_service_model = providers.Singleton(
        ServiceModel,
        host=config.merchant_service_host,
        port=config.merchant_service_port
    )

    __db_connection = providers.Singleton(PostgresDbConnection, __db_config)

    inventory_repository_provider = providers.Singleton(InventoryRepository, db_connection=__db_connection)
