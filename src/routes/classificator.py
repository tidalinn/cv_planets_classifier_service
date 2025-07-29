import cv2
import numpy as np
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, File

from src.containers import AppContainer
from src.containers.classificator import Classificator
from src.utils.logger import LOGGER

router = APIRouter(prefix='/classificator', tags=['classificator'])


@router.get('/tags')
@inject
async def tags_list(
    service: Classificator = Depends(Provide[AppContainer.classificator])
) -> dict[str, list[str]]:

    LOGGER.info(f'Tags list: {service.classes}')
    return {'tags': service.classes}


@router.post('/predict')
@inject
async def predict(
    image_file: bytes = File(...),
    service: Classificator = Depends(Provide[AppContainer.classificator]),
) -> dict[str, list[str]]:
    image = cv2.imdecode(np.frombuffer(image_file, np.uint8), cv2.IMREAD_COLOR)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    tags = service.predict(image)

    LOGGER.info(f'Predicted tags: {tags}')
    return {'tags': tags}


@router.post('/predict_proba')
@inject
async def predict_proba(
    image_file: bytes = File(...),
    service: Classificator = Depends(Provide[AppContainer.classificator]),
) -> dict[str, float]:
    image = cv2.imdecode(np.frombuffer(image_file, np.uint8), cv2.IMREAD_COLOR)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return service.predict_proba(image)


@router.get('/healthcheck')
async def health_check() -> dict[str, str]:
    return {'status': 'ok'}
