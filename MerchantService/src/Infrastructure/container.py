from dependency_injector import containers, providers

from src.Repositories import MerchantRepository
from src.DbConnections import DbConfig, PostgresDbConnection
import src.Infrastructure.settings as settings


class Container(containers.DeclarativeContainer):
    config: settings.Settings = providers.Configuration()

    __db_config = providers.Singleton(
        DbConfig,
        host=config.postgres_host,
        user=config.postgres_user,
        database=config.postgres_database,
        password=config.postgres_password
    )

    __db_connection = providers.Singleton(PostgresDbConnection, __db_config)

    merchant_repository_provider = providers.Singleton(MerchantRepository, db_connection=__db_connection)
