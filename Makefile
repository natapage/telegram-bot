.PHONY: install run clean

install:
	uv sync

run:
	uv run python -m src.main

clean:
	rm -rf __pycache__ .venv logs/*.log
