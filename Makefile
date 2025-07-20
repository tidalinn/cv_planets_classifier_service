.PHONY: run.inference venv.remove dvc.add_files dvc.get_files down run.prod run.dev run.tests run.tests.coverage_report

include .env
export

URL_MODELLING := ssh://git@gitlab.deepschool.ru:30022/dl-deploy2/p.kukhtenkova/final-project-modelling.git

VENV     := ~/.$(INFERENCE_IMAGE)
VENV_DVC := $(VENV)/bin/dvc
VENV_PIP := $(VENV)/bin/pip


# --- SERVICE ---

run.inference:
	uvicorn src.app:create_app --host 0.0.0.0 --port 80


# --- VENV ---

venv.create:
ifeq ($(wildcard $(VENV)/),)
	python3 -m venv $(VENV)
	$(VENV_PIP) install --no-cache-dir -r requirements/requirements-dvc.txt
	$(VENV_PIP) install --upgrade pip
ifeq ($(STAGE),dev)
	$(VENV_PIP) install --no-cache-dir -r requirements/requirements-dev.txt
endif
endif

venv.remove:
	rm -rf $(VENV)


# --- DVC ---

dvc.connect:
	ssh $(STAGING_USERNAME)@$(STAGING_HOST)

dvc.init: venv.create
ifeq ($(wildcard .dvc/),)
	$(VENV_DVC) init
	$(VENV_DVC) remote add --default $(STAGING_HOST) ssh://$(STAGING_HOST)/home/$(STAGING_USERNAME)/fp_service
	$(VENV_DVC) remote modify $(STAGING_HOST) user $(STAGING_USERNAME)
	$(VENV_DVC) remote list
	$(VENV_DVC) config core.autostage true
endif

dvc.add_files: dvc.init
	$(VENV_DVC) add .env
	$(VENV_DVC) push

dvc.get_files: dvc.init
	$(VENV_DVC) import $(URL_MODELLING) output/best/classificator.onnx -o models/classificator.onnx --rev dev
	$(VENV_DVC) import $(URL_MODELLING) output/encoder/mlb.pkl -o models/mlb.pkl --rev dev


# --- DOCKER ---

down:
	docker compose down --volumes --remove-orphans

run.prod:
	TARGET_STAGE=prod docker compose up --build

run.dev:
	TARGET_STAGE=dev docker compose up --build


# --- TESTS ---

run.tests:
	docker exec -e PYTHONPATH=/app -it $(INFERENCE_NAME) pytest /app/tests

run.tests.coverage_report:
	docker exec -e PYTHONPATH=/app -it $(INFERENCE_NAME) pytest --cov=src --cov-report html /app/tests/
