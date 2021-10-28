import uvicorn
from fastapi import FastAPI

from src.Infrastructure import Settings, Container
import src.endpoints as endpoints


def create_app() -> FastAPI:
    settings = Settings()

    container = Container()
    container.config.from_pydantic(settings)

    app = FastAPI()

    container.wire(modules=[endpoints])

    app.container = container
    app.include_router(endpoints.router)

    return app


app = create_app()

if __name__ == '__main__':
    uvicorn.run('src.application:app', host='0.0.0.0', port=8000, reload=True)
