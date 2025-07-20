from pathlib import Path
from typing import Dict, List, Tuple, Union

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
    classes: Dict[str, int]


class DataConfig(BaseValidatedConfig):
    img_size: Tuple[int, int]
    mean: List[float]
    std: List[float]


class ONNXConfig(BaseValidatedConfig):
    providers: List[str]


class ProjectConfig(BaseValidatedConfig):
    classificator: ClassificatorConfig
    data: DataConfig  # noqa: WPS110
    onnx: ONNXConfig

    @classmethod
    def from_yaml(cls, path: Union[str, Path]) -> 'ProjectConfig':
        config = OmegaConf.to_container(OmegaConf.load(path), resolve=True)
        return cls(**config)
