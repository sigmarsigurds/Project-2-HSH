from src.Infrastructure import Settings, Container
import src.Entities.transaction_transceiver as transceiver_file

print("Ég er til")

def main():

    settings = Settings()

    container = Container()
    container.config.from_pydantic(settings)

    transaction_transceiver: transceiver_file.TransactionTransceiver = container.transaction_transceiver_provider()

    transaction_transceiver.start()


if __name__ == "__main__":
    main()
