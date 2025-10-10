.PHONY: install run clean

install:
	uv sync

run:
	uv run python src/main.py

clean:
	rm -rf __pycache__ .venv logs/*.log
