.PHONY: install run run-api test-api api-docs clean format lint fix test test-cov

install:
	uv sync

run:
	uv run python -m src.main

run-api:
	uv run python -m src.api_main

test-api:
	@echo "Testing API endpoints..."
	@echo "\n=== Health Check ==="
	@curl -s http://localhost:8000/health | python -m json.tool || echo "Error: Make sure API is running (make run-api)"
	@echo "\n=== Stats (day) ==="
	@curl -s "http://localhost:8000/stats?period=day" | python -m json.tool || echo "Error: API not responding"
	@echo "\n=== Stats (week) ==="
	@curl -s "http://localhost:8000/stats?period=week" | python -m json.tool || echo "Error: API not responding"
	@echo "\n=== Stats (month) ==="
	@curl -s "http://localhost:8000/stats?period=month" | python -m json.tool || echo "Error: API not responding"

api-docs:
	@echo "API Documentation available at:"
	@echo "  Swagger UI: http://localhost:8000/docs"
	@echo "  ReDoc:      http://localhost:8000/redoc"
	@echo "\nMake sure API is running: make run-api"

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

# Frontend commands
.PHONY: frontend-install frontend-dev frontend-build frontend-lint frontend-test

frontend-install:
	cd frontend && pnpm install

frontend-dev:
	cd frontend && pnpm dev

frontend-build:
	cd frontend && pnpm build

frontend-lint:
	cd frontend && pnpm lint && pnpm format:check && pnpm type-check

frontend-test:
	cd frontend && pnpm test

# Docker commands (локальная сборка)
.PHONY: docker-up docker-down docker-build docker-logs docker-status docker-clean

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

docker-build:
	docker-compose build

docker-logs:
	docker-compose logs -f

docker-status:
	docker-compose ps

docker-clean:
	docker-compose down -v
	docker system prune -f

# Docker commands (использование образов из GitHub Container Registry)
.PHONY: docker-pull docker-up-registry docker-down-registry docker-logs-registry docker-status-registry

docker-pull:
	docker-compose -f docker-compose.registry.yml pull

docker-up-registry:
	docker-compose -f docker-compose.registry.yml up -d

docker-down-registry:
	docker-compose -f docker-compose.registry.yml down

docker-logs-registry:
	docker-compose -f docker-compose.registry.yml logs -f

docker-status-registry:
	docker-compose -f docker-compose.registry.yml ps
