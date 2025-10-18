# Makefile для управления Telegram Bot системой

.PHONY: help build up down restart logs status clean backup restore

# Цвета для вывода
RED=\033[0;31m
GREEN=\033[0;32m
YELLOW=\033[0;33m
BLUE=\033[0;34m
NC=\033[0m # No Color

# Конфигурация
COMPOSE_FILE=docker-compose.yml
COMPOSE_DEV=docker-compose.dev.yml
COMPOSE_PROD=docker-compose.prod.yml
BACKUP_DIR=backups
DATE=$(shell date +%Y%m%d_%H%M%S)

help: ## Показать справку по командам
	@echo "$(GREEN)Доступные команды:$(NC)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(BLUE)%-20s$(NC) %s\n", $$1, $$2}'

# =============================================================================
# DEVELOPMENT
# =============================================================================

dev-build: ## Собрать образы для разработки
	@echo "$(YELLOW)Сборка образов для разработки...$(NC)"
	docker-compose -f $(COMPOSE_FILE) -f $(COMPOSE_DEV) build

dev-up: ## Запустить в режиме разработки
	@echo "$(GREEN)Запуск в режиме разработки...$(NC)"
	docker-compose -f $(COMPOSE_FILE) -f $(COMPOSE_DEV) up -d
	@echo "$(GREEN)✓ Сервисы запущены$(NC)"
	@echo "  API:      http://localhost:8004"
	@echo "  Frontend: http://localhost:3004"

dev-down: ## Остановить в режиме разработки
	@echo "$(RED)Остановка сервисов разработки...$(NC)"
	docker-compose -f $(COMPOSE_FILE) -f $(COMPOSE_DEV) down

dev-logs: ## Показать логи (разработка)
	docker-compose -f $(COMPOSE_FILE) -f $(COMPOSE_DEV) logs -f

# =============================================================================
# PRODUCTION
# =============================================================================

prod-pull: ## Загрузить образы из registry
	@echo "$(YELLOW)Загрузка образов из registry...$(NC)"
	docker-compose -f $(COMPOSE_FILE) pull
	@echo "$(GREEN)✓ Образы загружены$(NC)"

prod-up: ## Запустить в production режиме
	@echo "$(GREEN)Запуск в production режиме...$(NC)"
	docker-compose -f $(COMPOSE_FILE) -f $(COMPOSE_PROD) up -d
	@echo "$(GREEN)✓ Сервисы запущены$(NC)"
	@echo "  API:      http://89.223.67.136:8004"
	@echo "  Frontend: http://89.223.67.136:3004"

prod-down: ## Остановить production сервисы
	@echo "$(RED)Остановка production сервисов...$(NC)"
	docker-compose -f $(COMPOSE_FILE) -f $(COMPOSE_PROD) down

prod-update: prod-pull ## Обновить production сервисы
	@echo "$(YELLOW)Обновление production сервисов...$(NC)"
	docker-compose -f $(COMPOSE_FILE) -f $(COMPOSE_PROD) up -d --force-recreate
	docker image prune -f
	@echo "$(GREEN)✓ Сервисы обновлены$(NC)"

# =============================================================================
# BASIC OPERATIONS
# =============================================================================

up: ## Запустить все сервисы (стандартно)
	@echo "$(GREEN)Запуск сервисов...$(NC)"
	docker-compose up -d
	@echo "$(GREEN)✓ Сервисы запущены$(NC)"

down: ## Остановить все сервисы
	@echo "$(RED)Остановка сервисов...$(NC)"
	docker-compose down

restart: ## Перезапустить все сервисы
	@echo "$(YELLOW)Перезапуск сервисов...$(NC)"
	docker-compose restart
	@echo "$(GREEN)✓ Сервисы перезапущены$(NC)"

restart-bot: ## Перезапустить бота
	@echo "$(YELLOW)Перезапуск бота...$(NC)"
	docker-compose restart bot
	@echo "$(GREEN)✓ Бот перезапущен$(NC)"

restart-api: ## Перезапустить API
	@echo "$(YELLOW)Перезапуск API...$(NC)"
	docker-compose restart api
	@echo "$(GREEN)✓ API перезапущен$(NC)"

restart-frontend: ## Перезапустить Frontend
	@echo "$(YELLOW)Перезапуск Frontend...$(NC)"
	docker-compose restart frontend
	@echo "$(GREEN)✓ Frontend перезапущен$(NC)"

# =============================================================================
# MONITORING
# =============================================================================

status: ## Показать статус сервисов
	@echo "$(BLUE)Статус сервисов:$(NC)"
	docker-compose ps

logs: ## Показать логи всех сервисов
	docker-compose logs -f

logs-bot: ## Показать логи бота
	docker-compose logs -f bot

logs-api: ## Показать логи API
	docker-compose logs -f api

logs-frontend: ## Показать логи Frontend
	docker-compose logs -f frontend

health: ## Проверить здоровье сервисов
	@echo "$(BLUE)Проверка здоровья сервисов:$(NC)"
	@echo -n "  API:      "
	@curl -sf http://localhost:8004/health >/dev/null && echo "$(GREEN)✓ OK$(NC)" || echo "$(RED)✗ FAIL$(NC)"
	@echo -n "  Frontend: "
	@curl -sf http://localhost:3004 >/dev/null && echo "$(GREEN)✓ OK$(NC)" || echo "$(RED)✗ FAIL$(NC)"

stats: ## Показать статистику использования ресурсов
	docker stats --no-stream

# =============================================================================
# DATABASE
# =============================================================================

db-backup: ## Создать резервную копию базы данных
	@echo "$(YELLOW)Создание резервной копии...$(NC)"
	@mkdir -p $(BACKUP_DIR)
	docker cp telegram-api:/app/data/telegram_bot.db $(BACKUP_DIR)/telegram_bot_$(DATE).db
	@echo "$(GREEN)✓ Резервная копия создана: $(BACKUP_DIR)/telegram_bot_$(DATE).db$(NC)"

db-restore: ## Восстановить базу данных (использование: make db-restore FILE=backup.db)
	@if [ -z "$(FILE)" ]; then \
		echo "$(RED)Ошибка: укажите файл через FILE=путь/к/файлу$(NC)"; \
		exit 1; \
	fi
	@echo "$(YELLOW)Восстановление базы данных из $(FILE)...$(NC)"
	docker cp $(FILE) telegram-api:/app/data/telegram_bot.db
	docker-compose restart api bot
	@echo "$(GREEN)✓ База данных восстановлена$(NC)"

db-list-backups: ## Показать список резервных копий
	@echo "$(BLUE)Доступные резервные копии:$(NC)"
	@ls -lh $(BACKUP_DIR)/telegram_bot_*.db 2>/dev/null || echo "  Резервные копии не найдены"

# =============================================================================
# MAINTENANCE
# =============================================================================

clean: ## Удалить остановленные контейнеры и неиспользуемые образы
	@echo "$(YELLOW)Очистка...$(NC)"
	docker-compose down
	docker image prune -f
	@echo "$(GREEN)✓ Очистка завершена$(NC)"

clean-all: ## Полная очистка (включая volumes)
	@echo "$(RED)ВНИМАНИЕ: Будут удалены все данные!$(NC)"
	@echo "Нажмите Ctrl+C для отмены, Enter для продолжения"
	@read confirm
	docker-compose down -v
	docker image prune -a -f
	docker volume prune -f
	@echo "$(GREEN)✓ Полная очистка завершена$(NC)"

clean-logs: ## Очистить логи
	@echo "$(YELLOW)Очистка логов...$(NC)"
	docker-compose exec api sh -c "rm -rf /app/logs/*.log" 2>/dev/null || true
	docker-compose exec bot sh -c "rm -rf /app/logs/*.log" 2>/dev/null || true
	@echo "$(GREEN)✓ Логи очищены$(NC)"

# =============================================================================
# SHELL ACCESS
# =============================================================================

shell-bot: ## Открыть shell в контейнере бота
	docker-compose exec bot bash

shell-api: ## Открыть shell в контейнере API
	docker-compose exec api bash

shell-frontend: ## Открыть shell в контейнере Frontend
	docker-compose exec frontend sh

# =============================================================================
# CONFIGURATION
# =============================================================================

env-example: ## Создать .env файл из примера
	@if [ -f .env ]; then \
		echo "$(RED)Файл .env уже существует!$(NC)"; \
		echo "Используйте 'make env-overwrite' для перезаписи"; \
	else \
		cp .env.example .env; \
		echo "$(GREEN)✓ Файл .env создан из .env.example$(NC)"; \
		echo "$(YELLOW)Не забудьте заполнить необходимые переменные!$(NC)"; \
	fi

env-overwrite: ## Перезаписать .env файл из примера
	@echo "$(YELLOW)Перезапись .env файла...$(NC)"
	cp .env.example .env
	@echo "$(GREEN)✓ Файл .env перезаписан$(NC)"

env-validate: ## Проверить конфигурацию
	@echo "$(BLUE)Проверка конфигурации...$(NC)"
	docker-compose config > /dev/null && echo "$(GREEN)✓ Конфигурация корректна$(NC)" || echo "$(RED)✗ Ошибка в конфигурации$(NC)"

# =============================================================================
# SECRETS (PRODUCTION)
# =============================================================================

secrets-setup: ## Создать структуру для secrets
	@echo "$(YELLOW)Создание структуры для secrets...$(NC)"
	@mkdir -p secrets
	@touch secrets/telegram_bot_token.txt
	@touch secrets/openai_api_key.txt
	@chmod 600 secrets/*.txt
	@echo "$(GREEN)✓ Структура создана$(NC)"
	@echo "$(YELLOW)Не забудьте заполнить файлы секретов:$(NC)"
	@echo "  secrets/telegram_bot_token.txt"
	@echo "  secrets/openai_api_key.txt"

# =============================================================================
# TESTING
# =============================================================================

test: ## Запустить тесты
	@echo "$(YELLOW)Запуск тестов...$(NC)"
	docker-compose exec api pytest tests/
	@echo "$(GREEN)✓ Тесты завершены$(NC)"

# =============================================================================
# UTILITIES
# =============================================================================

config: ## Показать полную конфигурацию
	docker-compose config

inspect-bot: ## Показать информацию о контейнере бота
	docker inspect telegram-bot

inspect-api: ## Показать информацию о контейнере API
	docker inspect telegram-api

inspect-frontend: ## Показать информацию о контейнере Frontend
	docker inspect telegram-frontend

network-inspect: ## Показать информацию о сети
	docker network inspect telegram-network

volume-inspect: ## Показать информацию о volumes
	@echo "$(BLUE)Bot Data:$(NC)"
	@docker volume inspect telegram-bot-data
	@echo "$(BLUE)API Data:$(NC)"
	@docker volume inspect telegram-api-data
