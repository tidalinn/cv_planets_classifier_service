import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from src.app import set_routers
from src.configs import ProjectConfig
from src.constants import PATH_CONFIGS, PATH_TESTS
from src.containers import AppContainer
from src.routes import classificator

SCOPE = 'session'


@pytest.fixture(scope=SCOPE)
def fake_image():
    path_image = PATH_TESTS / 'images' / 'image.jpg'
    with path_image.open('rb') as file_image:
        yield file_image.read()


@pytest.fixture(scope=SCOPE)
def fake_config():
    return ProjectConfig.from_yaml(PATH_CONFIGS / 'project.yml')


@pytest.fixture(scope=SCOPE)
def fake_container(fake_config):
    container = AppContainer()
    container.config.from_dict(fake_config.dict())
    container.wire([classificator])
    yield
    container.unwire()


@pytest.fixture(scope=SCOPE)
def fake_app(fake_container):
    app = FastAPI()
    set_routers(app)
    return app


@pytest.fixture(scope=SCOPE)
def fake_client(fake_app):
    return TestClient(fake_app)
