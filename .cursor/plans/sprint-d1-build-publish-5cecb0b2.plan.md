<!-- 5cecb0b2-6171-484e-bdc0-5bb18d609519 d71c8792-bc4c-4ad5-999a-396997d62689 -->
# План Спринта D1: Build & Publish

## Обзор

Настроить автоматическую сборку и публикацию Docker образов (bot, api, frontend) в GitHub Container Registry (ghcr.io) при push в main ветку. Образы будут публичными и доступными без авторизации.

## Компоненты

### 1. Документация GitHub Actions

**Файл**: `devops/doc/guides/github-actions-intro.md`

Создать краткую инструкцию:

- Что такое GitHub Actions и workflow
- Основные концепции: jobs, steps, actions
- Triggers: push, pull_request, workflow_dispatch
- Работа с Pull Requests и проверка изменений
- GitHub Container Registry (ghcr.io)
- Public vs Private образы
- Matrix strategy для параллельной сборки

### 2. GitHub Actions Workflow

**Файл**: `.github/workflows/build.yml`

Ключевые элементы:

- **Trigger**: `push` в `main` ветку
- **Matrix strategy**: 3 образа (bot, api, frontend)
- **Docker BuildKit**: включить для кэширования layers
- **Кэширование**: использовать `actions/cache` для Docker layers
- **Тегирование**: 
  - `latest` - для последней версии
  - `sha-{SHORT_SHA}` - для конкретного коммита
- **Registry**: ghcr.io/natapage/telegram-bot-{service}
- **Permissions**: публичный доступ к образам

Особенности сборки:

- `bot` и `api`: context=`.`, dockerfile=`Dockerfile.{service}`
- `frontend`: context=`./frontend`, dockerfile=`../Dockerfile.frontend`

### 3. Docker Compose для Registry

**Файл**: `docker-compose.registry.yml`

Новый файл для использования образов из ghcr.io:

- Замена `build` на `image: ghcr.io/natapage/telegram-bot-{service}:latest`
- Сохранить все volumes и переменные окружения
- Добавить комментарии для понимания различий

**Обновить**: `docker-compose.yml`

- Добавить комментарии о локальной сборке
- Указать на существование `docker-compose.registry.yml`

### 4. Makefile команды

Добавить в `Makefile`:

```makefile
docker-pull:        # Pull образов из registry
docker-up-registry: # Запуск с образами из registry
```

### 5. Инструкция по публикации образов

**Файл**: `devops/doc/guides/github-registry-setup.md`

Пошаговая инструкция:

- Настройка permissions для GitHub Actions в репозитории
- Settings → Actions → General → Workflow permissions → Read and write
- Settings → Packages → для настройки видимости пакетов (public)
- Как работает автоматическая публикация
- Проверка опубликованных образов
- Команды для локального pull

### 6. Документация использования

**Обновить**: `README.md`

Добавить:

- Badge статуса сборки: `![Build](https://github.com/natapage/telegram-bot/actions/workflows/build.yml/badge.svg)`
- Секцию "Использование Docker образов из Registry"
- Команды: `docker-compose -f docker-compose.registry.yml up`
- Ссылки на образы в ghcr.io

**Создать**: `DOCKER_QUICKSTART.md`

Быстрая инструкция:

- Локальная сборка vs Registry образы
- Команды для обоих вариантов
- Когда использовать какой подход

### 7. План спринта

**Файл**: `devops/doc/plans/d1-build-publish-plan.md`

Детальный план с описанием всех шагов, решений и примерами.

### 8. Обновление roadmap

**Обновить**: `devops/doc/devops-roadmap.md`

- Изменить статус D1 на 🚧 In Progress
- Добавить ссылку на план: `[план](plans/d1-build-publish-plan.md)`

## Тестирование

После реализации:

1. Проверить синтаксис workflow файла
2. Создать тестовый коммит и push в main
3. Проверить запуск GitHub Actions
4. Проверить публикацию образов в ghcr.io
5. Локально pull образы: `docker pull ghcr.io/natapage/telegram-bot-bot:latest`
6. Запустить через registry: `docker-compose -f docker-compose.registry.yml up`
7. Убедиться что все сервисы работают

## MVP Подход

**Включено**:

- ✅ Автоматическая сборка при push в main
- ✅ Публикация в ghcr.io
- ✅ Public доступ к образам
- ✅ Тегирование latest и sha
- ✅ Matrix strategy для параллельной сборки
- ✅ Базовое кэширование Docker layers

**Не включено** (для будущих спринтов):

- ❌ Lint checks в CI
- ❌ Unit/Integration тесты в CI
- ❌ Security scanning
- ❌ Multi-platform builds (amd64/arm64)
- ❌ Версионные теги (v1.0.0)
- ❌ Уведомления о сборке

## Ключевые файлы

Создать:

- `.github/workflows/build.yml`
- `docker-compose.registry.yml`
- `devops/doc/guides/github-actions-intro.md`
- `devops/doc/guides/github-registry-setup.md`
- `devops/doc/plans/d1-build-publish-plan.md`
- `DOCKER_QUICKSTART.md`

Обновить:

- `README.md`
- `docker-compose.yml` (комментарии)
- `Makefile`
- `devops/doc/devops-roadmap.md`

### To-dos

- [ ] Создать документацию по GitHub Actions (devops/doc/guides/github-actions-intro.md)
- [ ] Создать инструкцию по настройке GitHub Container Registry (devops/doc/guides/github-registry-setup.md)
- [ ] Создать GitHub Actions workflow для сборки и публикации образов (.github/workflows/build.yml)
- [ ] Создать docker-compose.registry.yml для использования образов из ghcr.io
- [ ] Добавить команды для работы с registry в Makefile
- [ ] Создать DOCKER_QUICKSTART.md с инструкциями по использованию образов
- [ ] Обновить README.md с badge и инструкциями по использованию registry образов
- [ ] Создать детальный план спринта (devops/doc/plans/d1-build-publish-plan.md)
- [ ] Обновить devops roadmap со статусом D1