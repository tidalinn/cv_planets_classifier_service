.PHONY: *

INFERENCE_IMAGE := fp-service-polina-kukhtenkova


# --- SERVICE ---

run.inference:
	uvicorn src.app:create_app --host 0.0.0.0 --port 80


# --- DOCKER ---

run.prod:
	TARGET_STAGE=prod docker compose up --build

run.dev:
	TARGET_STAGE=dev docker compose up --build


# --- TESTS ---

run.tests:
	docker exec -e PYTHONPATH=/app -it $(INFERENCE_NAME) pytest /app/tests

run.tests.coverage_report:
	docker exec -e PYTHONPATH=/app -it $(INFERENCE_NAME) pytest --cov=src --cov-report html /app/tests/
