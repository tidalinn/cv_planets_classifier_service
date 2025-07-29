from dependency_injector import containers, providers

from src.configs import ProjectConfig
from src.containers.classificator import Classificator


class AppContainer(containers.DeclarativeContainer):
    config = providers.Configuration()
    config_project = providers.Callable(
        lambda cfg: ProjectConfig(**cfg),
        cfg=config,
    )

    classificator = providers.Singleton(
        Classificator,
        config=config_project
    )
