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
	uv run python ../agent-dev-harness/python-styleguide/docstring_length.py .
	uv run mypy .

type-check:
	uv run mypy .

notebook:
	uv run jupyter notebook k_nearest_neighbors.ipynb

docker-build:
	docker compose build

docker-up:
	docker compose up -d

docker-down:
	docker compose down
