from dependency_injector import containers, providers

from src.Repositories import TransactionRepository
from src.Validators import CreditCardValidator
from src.Entities import Transaction, TransactionTransceiver, EmailConstructor

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

    __credit_card_validator = providers.Singleton(CreditCardValidator)

    __transaction_repository_provider = providers.Singleton(TransactionRepository, db_connection=__db_connection)

    __email_constructor_provider = providers.Singleton(EmailConstructor, db_connection=__db_connection)

    __transaction_provider = providers.Singleton(
        Transaction,
        credit_card_validator=__credit_card_validator,
        transaction_repository=__transaction_repository_provider
    )

    transaction_transceiver_provider = providers.Singleton(
        TransactionTransceiver,
        transaction=__transaction_provider,
        email_constructor=__email_constructor_provider,
        rabbitmq_server_host=config.rabbitmq_server_host,
    )
