.PHONY: install generate-profiles generate-events generate-ground-truth run-pipeline test lint format dashboard api docker-up docker-down

install:
	python -m pip install -r requirements.txt

generate-profiles:
	python -m src.data_generation.generate_profiles

generate-events:
	python -m src.data_generation.generate_events

generate-ground-truth:
	python -m src.data_generation.generate_ground_truth

run-pipeline:
	python -m src.pipeline.run_all

test:
	python -m pytest

lint:
	python -m ruff check .

format:
	python -m ruff format .

dashboard:
	streamlit run src/dashboard/app.py

api:
	uvicorn src.api.main:app --reload

docker-up:
	docker compose up --build

docker-down:
	docker compose down

