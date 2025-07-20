.PHONY: run.inference dvc.get.files run.prod run.dev run.tests run.tests.coverage_report

include .env
export

URL_MODELLING := ssh://git@gitlab.deepschool.ru:30022/dl-deploy2/p.kukhtenkova/final-project-modelling.git


# --- SERVICE ---

run.inference:
	uvicorn src.app:create_app --host 0.0.0.0 --port 80


# --- DVC ---

dvc.connect:
	ssh $(STAGING_USERNAME)@$(STAGING_HOST)

dvc.get.files:
ifeq ($(wildcard .dvc/),)
	dvc init --no-scm
endif
	dvc import $(URL_MODELLING) output/best/classificator.onnx -o models/classificator.onnx --rev dev
	dvc import $(URL_MODELLING) output/encoder/mlb.pkl -o models/mlb.pkl --rev dev


# --- DOCKER ---

run:
	@SSH_PRIVATE_KEY="$$(cat ~/.ssh/id_rsa)" \
	TARGET_STAGE=$(TARGET_STAGE) docker compose up --build

run.prod:
	make run TARGET_STAGE=prod

run.dev:
	make run TARGET_STAGE=dev


# --- TESTS ---

run.tests:
	docker exec -e PYTHONPATH=/app -it $(INFERENCE_NAME) pytest /app/tests

run.tests.coverage_report:
	docker exec -e PYTHONPATH=/app -it $(INFERENCE_NAME) pytest --cov=src --cov-report html /app/tests/
