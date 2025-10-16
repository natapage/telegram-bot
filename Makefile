.PHONY: install run clean format lint fix test test-cov

install:
	uv sync

run:
	uv run python -m src.main

format:
	uv run ruff format src/

lint:
	uv run ruff check src/ && uv run mypy src/

fix:
	uv run ruff check src/ --fix

test:
	uv run pytest tests/ -v

test-cov:
	uv run pytest tests/ -v --cov=src --cov-report=term-missing

clean:
	rm -rf __pycache__ .venv logs/*.log
