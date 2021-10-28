import uvicorn
from fastapi import FastAPI
from Infrastructure.container import Container
from Infrastructure.settings import Settings
import endpoints


def create_app() -> FastAPI:

    settings = Settings("./Infrastructure/.env")
    container = Container()
    container.config.from_pydantic(settings)

    container.wire(modules=[endpoints])

    app = FastAPI()
    app.container = container
    app.include_router(endpoints.router)

    return app


app = create_app()

if __name__ == "__main__":
    uvicorn.run("application:app", host="0.0.0.0", port=8000, reload=True)
