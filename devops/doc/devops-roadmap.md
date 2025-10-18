# DevOps Roadmap

## Обзор

Этот роадмап описывает развитие DevOps процессов для проекта telegram-bot.
Используется MVP подход: фокус на простоте и скорости, без преждевременной оптимизации.

Цель: пройти путь от локального отдельного запуска до удаленного сервера с автоматическим развертыванием максимально быстро.

## Спринты

| Код | Описание | Статус | План |
|-----|----------|--------|------|
| D0 | Basic Docker Setup | ✅ Completed | [план](plans/d0-docker-setup-plan.md) |
| D1 | Build & Publish | 🚧 In Progress | [план](plans/d1-build-publish-plan.md) |
| D2 | Развертывание на сервер | 📋 Planned | - |
| D3 | Auto Deploy | 📋 Planned | - |

**Легенда статусов:**
- 📋 Planned - запланировано
- 🚧 In Progress - в работе
- ✅ Completed - завершено

---

## Спринт D0: Basic Docker Setup

**Дата завершения**: 18 октября 2025
**Статус**: ✅ Завершен и протестирован

### Цели

Запустить все сервисы локально через docker-compose одной командой.

### Что реализовано

✅ **Docker-образы**:
- `Dockerfile.bot` - Telegram бот (Python 3.11 + UV)
- `Dockerfile.api` - FastAPI backend (Python 3.11 + UV)
- `Dockerfile.frontend` - Next.js frontend (Node 20 + pnpm)

✅ **Docker Compose**:
- 3 сервиса: bot, api, frontend
- SQLite база данных с volume для персистентности
- Правильные зависимости между сервисами
- Restart policy: `unless-stopped`

✅ **Конфигурация**:
- `.dockerignore` (корневой и для frontend)
- `.env.example` с шаблоном переменных
- Makefile команды для управления Docker

✅ **Документация**:
- README.md обновлен с инструкциями Docker
- Детальный план: [plans/d0-docker-setup-plan.md](plans/d0-docker-setup-plan.md)
- Отчет о тестировании: [reports/d0-testing-report.md](reports/d0-testing-report.md)
- Итоговая сводка: [reports/d0-summary.md](reports/d0-summary.md)

### Технические решения

- **База данных**: SQLite (MVP подход, простота)
- **Build strategy**: Single-stage builds (скорость разработки)
- **Volumes**: prompts, logs, telegram_bot.db
- **Порты**: API (8000), Frontend (3001)

### Результаты тестирования

- ✅ Сборка образов: ~98 секунд
- ✅ Все сервисы запущены и работают
- ✅ API health check: OK
- ✅ Frontend доступен и отдает страницу
- ✅ Bot запущен

**Найдено и исправлено 3 проблемы** во время тестирования (детали в отчете)

---

## Спринт D1: Build & Publish

**Дата начала**: 18 октября 2025
**Статус**: 🚧 В работе

### Цели

Автоматическая сборка и публикация Docker образов в GitHub Container Registry.

### Состав работ

**Реализовано**:
- ✅ Создан GitHub Actions workflow `.github/workflows/build.yml`
- ✅ Настроен trigger: push в main + pull_request
- ✅ Matrix strategy для параллельной сборки 3 образов (bot, api, frontend)
- ✅ Кэширование Docker layers для ускорения
- ✅ Тегирование: latest и sha-XXXXXX
- ✅ Создан `docker-compose.registry.yml` для использования образов из ghcr.io
- ✅ Обновлен Makefile с командами для registry
- ✅ Создана документация: github-actions-intro.md, github-registry-setup.md
- ✅ Создан DOCKER_QUICKSTART.md
- ✅ Обновлен README.md с badge и инструкциями

**В процессе**:
- ⏳ Тестирование workflow в реальных условиях
- ⏳ Публикация образов и настройка public access

### Технические решения

- **CI/CD**: GitHub Actions с matrix strategy
- **Registry**: GitHub Container Registry (ghcr.io)
- **Visibility**: Public образы (доступны без авторизации)
- **Кэширование**: GitHub Actions Cache для Docker layers
- **Теги**: latest (auto-update), sha (immutable)
- **Два режима**: локальная сборка (dev) и registry (prod)

**Ожидаемые файлы:**
- `.github/workflows/build.yml` ✅
- `docker-compose.registry.yml` ✅
- `devops/doc/guides/github-actions-intro.md` ✅
- `devops/doc/guides/github-registry-setup.md` ✅
- `devops/doc/plans/d1-build-publish-plan.md` ✅
- `DOCKER_QUICKSTART.md` ✅
- Обновленный `README.md` с badges ✅
- Обновленный `Makefile` ✅

---

## Спринт D2: Развертывание на сервер

### Цели

Развернуть приложение на удаленном сервере вручную (пошаговая инструкция).

**Контекст:** Готовый сервер предоставлен (адрес + SSH ключ, Docker установлен).

### Состав работ

- Создать пошаговую инструкцию для ручного деплоя
- SSH подключение к серверу с помощью SSH ключа
- Копирование docker-compose.yml и .env на сервер
- docker login к ghcr.io
- docker-compose pull - загрузка образов
- docker-compose up -d - запуск сервисов
- Запуск миграций базы данных
- Проверка работоспособности

**Ожидаемые файлы:**
- `devops/doc/guides/manual-deploy.md` (детальная пошаговая инструкция)
- `.env.production` (шаблон с описанием всех переменных)
- `devops/scripts/deploy-check.sh` (скрипт проверки работоспособности)

---

## Спринт D3: Auto Deploy

### Цели

Автоматическое развертывание на сервер через GitHub Actions по кнопке.

### Состав работ

- Создать GitHub Actions workflow `.github/workflows/deploy.yml`
- Настроить trigger: ручной запуск (workflow_dispatch)
- SSH подключение к серверу с помощью SSH ключа
- Pull новых версий образов
- Restart сервисов через docker-compose
- Создать инструкцию по настройке secrets (SSH_KEY, HOST, USER в GitHub Actions)
- Добавить уведомления о статусе деплоя

**Ожидаемые файлы:**
- `.github/workflows/deploy.yml`
- `devops/doc/guides/auto-deploy-setup.md` (настройка GitHub secrets)
- Обновленный `README.md` с кнопкой "Deploy"

---

## Планирование

Планирование каждого спринта выполняется в режиме **Plan Mode**. После выполнения спринта:
1. Создается детальный план в директории `devops/doc/plans/`
2. Обновляется ссылка на план в таблице спринтов выше
3. Статус спринта меняется на ✅ Completed

## Принципы

- **MVP подход**: простота и скорость важнее оптимизации
- **Итеративная разработка**: небольшие спринты с конкретными целями
- **Документирование**: каждый спринт сопровождается планом и инструкциями
- **Быстрый путь к production**: от локального запуска до автодеплоя за 4 спринта
