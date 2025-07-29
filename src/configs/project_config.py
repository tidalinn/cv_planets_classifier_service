from pathlib import Path
from typing import Union

from omegaconf import OmegaConf
from pydantic import BaseModel, ConfigDict


class BaseValidatedConfig(BaseModel):
    model_config = ConfigDict(
        extra='forbid',
        protected_namespaces=()
    )


class ClassificatorConfig(BaseValidatedConfig):
    path_model: str
    threshold: float
    classes: dict[str, int]


class DataConfig(BaseValidatedConfig):
    img_size: tuple[int, int]
    mean: list[float]
    std: list[float]


class ONNXConfig(BaseValidatedConfig):
    providers: list[str]


class ProjectConfig(BaseValidatedConfig):
    classificator: ClassificatorConfig
    data: DataConfig  # noqa: WPS110
    onnx: ONNXConfig

    @classmethod
    def from_yaml(cls, path: Union[str, Path]) -> 'ProjectConfig':
        config = OmegaConf.to_container(OmegaConf.load(path), resolve=True)
        return cls(**config)
