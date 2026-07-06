.PHONY: install api test lint format check type-check notebook docker-build docker-up docker-down

install:
	uv sync

api:
	uv run uvicorn src.app.api:app --reload

test:
	uv run pytest

lint:
	uv run ruff check .

format:
	uv run ruff format .

check:
	uv run ruff check .
	uv run ruff format --check .

type-check:
	uv run mypy src

notebook:
	uv run jupyter notebook k_nearest_neighbors.ipynb

docker-build:
	docker compose build

docker-up:
	docker compose up -d

docker-down:
	docker compose down
