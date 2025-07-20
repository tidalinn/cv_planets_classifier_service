import os
from pathlib import Path

PROJECT_NAME = 'planets-classifier'

PATH_PROJECT = Path(__file__).resolve().parents[1]
PATH_PROJECT_ROOT = Path(os.getenv('FP_MODELLING_ROOT', PATH_PROJECT))

PATH_CONFIGS = PATH_PROJECT_ROOT / 'configs'
PATH_TESTS = PATH_PROJECT_ROOT / 'tests'
PATH_LOGS = PATH_PROJECT_ROOT / 'logs'
