from fastapi import FastAPI

from src.configs import ProjectConfig
from src.constants import PATH_CONFIGS
from src.containers import AppContainer
from src.routes import classificator, metrics
from src.utils.logger import LOGGER
from src.utils.metrics import metrics_middleware
from src.utils.tracing import setup_tracer


def set_routers(app: FastAPI):
    app.include_router(classificator.router)
    app.include_router(metrics.router)


def create_app() -> FastAPI:
    config = ProjectConfig.from_yaml(PATH_CONFIGS / 'project.yml')

    container = AppContainer()
    container.config.from_dict(config.dict())
    container.wire([classificator])

    app = FastAPI()
    app.middleware('http')(metrics_middleware)
    set_routers(app)
    setup_tracer(app)

    LOGGER.info('Created app')

    return app
