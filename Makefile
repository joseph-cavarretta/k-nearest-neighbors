.PHONY: install lint format check notebook

install:
	uv sync

lint:
	uv run ruff check .

format:
	uv run ruff format .

check:
	uv run ruff check .
	uv run ruff format --check .

notebook:
	uv run jupyter notebook k_nearest_neighbors.ipynb
