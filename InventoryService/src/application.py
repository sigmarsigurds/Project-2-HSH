import uvicorn
import threading
from fastapi import FastAPI
from dependency_injector.wiring import inject, Provide


from src.Infrastructure import Settings, Container
import src.endpoints as endpoints

settings = Settings()


def create_app() -> FastAPI:

    container = Container()
    container.config.from_pydantic(settings)

    app = FastAPI()

    container.wire(modules=[endpoints])

    app.container = container
    app.include_router(endpoints.router)

    payment_queue_receiver = container.payment_queue_receiver_provider()

    thread = threading.Thread(target=payment_queue_receiver.start)
    thread.start()

    return app


app = create_app()


if __name__ == '__main__':



    uvicorn.run('src.application:app', host=settings.host, port=settings.port, reload=True)