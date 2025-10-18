# GitHub Actions: Введение

## Что такое GitHub Actions?

GitHub Actions — это встроенная CI/CD платформа GitHub, позволяющая автоматизировать процессы сборки, тестирования и развертывания прямо в репозитории.

### Основные преимущества

- **Интеграция с GitHub**: нативная интеграция с PR, Issues, коммитами
- **Бесплатно для публичных репозиториев**: неограниченные минуты выполнения
- **Marketplace**: тысячи готовых actions от сообщества
- **Matrix builds**: параллельная сборка нескольких конфигураций
- **Простота**: YAML конфигурация, понятный синтаксис

## Основные концепции

### Workflow (Рабочий процесс)

YAML файл в директории `.github/workflows/`, описывающий автоматизированный процесс.

```yaml
name: Build
on: [push]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: echo "Hello World"
```

### Jobs (Задачи)

Набор шагов (steps), выполняемых на одном runner. Jobs могут выполняться параллельно или последовательно.

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - run: npm test

  build:
    needs: test  # выполнится после test
    runs-on: ubuntu-latest
    steps:
      - run: npm build
```

### Steps (Шаги)

Отдельные задачи внутри job. Могут быть:
- **Action** (uses): готовое действие из Marketplace или локальное
- **Command** (run): команда shell

```yaml
steps:
  - uses: actions/checkout@v4        # action
  - run: npm install                  # command
  - uses: actions/upload-artifact@v4  # action
```

### Actions (Действия)

Переиспользуемые модули для выполнения типовых задач:
- `actions/checkout@v4` - клонирование репозитория
- `actions/setup-node@v4` - установка Node.js
- `docker/build-push-action@v5` - сборка и публикация Docker образов

## Triggers (Триггеры)

События, запускающие workflow.

### Push

Запуск при push в определенные ветки:

```yaml
on:
  push:
    branches:
      - main
      - develop
```

### Pull Request

Запуск при создании/обновлении PR:

```yaml
on:
  pull_request:
    branches:
      - main
```

**Типичный сценарий**: проверка сборки и тестов перед мёрджем.

### Workflow Dispatch

Ручной запуск workflow через UI GitHub:

```yaml
on:
  workflow_dispatch:
    inputs:
      environment:
        description: 'Environment to deploy'
        required: true
        default: 'staging'
```

**Использование**: деплой по кнопке, очистка кэша, и т.д.

### Комбинация триггеров

```yaml
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  workflow_dispatch:
```

## Работа с Pull Requests

### Проверка изменений перед мёрджем

```yaml
name: PR Check
on:
  pull_request:
    branches: [main]

jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Lint
        run: make lint
      - name: Test
        run: make test
```

### Branch Protection Rules

В Settings → Branches → Branch protection rules:
- Require status checks to pass before merging
- Require pull request reviews before merging

Это заставит все PR проходить через CI перед мёрджем.

## GitHub Container Registry (ghcr.io)

GitHub предоставляет бесплатный Docker registry для хранения образов.

### Преимущества ghcr.io

- **Бесплатно**: для публичных репозиториев
- **Интеграция**: привязка образов к репозиторию
- **Безопасность**: автоматическое сканирование уязвимостей
- **Удобство**: единая платформа для кода и образов

### Адрес образа

```
ghcr.io/OWNER/IMAGE_NAME:TAG
```

Примеры:
- `ghcr.io/natapage/telegram-bot-api:latest`
- `ghcr.io/natapage/telegram-bot-bot:sha-abc123`

### Public vs Private образы

**Public** (публичные):
- Доступны всем без авторизации
- `docker pull` работает без `docker login`
- Подходит для open source проектов

**Private** (приватные):
- Требуют авторизации для pull
- Используются для коммерческих/закрытых проектов
- Ограничения по storage (500 MB для бесплатного аккаунта)

### Настройка публичного доступа

После первой публикации образа:
1. Перейти в Packages (вкладка в профиле/репозитории)
2. Выбрать пакет
3. Package settings → Change visibility → Public

## Matrix Strategy

Параллельная сборка нескольких конфигураций.

### Пример: несколько версий Node.js

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        node-version: [16, 18, 20]
    steps:
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node-version }}
      - run: npm test
```

Запустит 3 параллельных job для Node.js 16, 18, 20.

### Пример: несколько Docker образов

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        service: [bot, api, frontend]
    steps:
      - name: Build ${{ matrix.service }}
        run: docker build -t my-${{ matrix.service }} .
```

Соберет 3 образа параллельно.

### Matrix с разными параметрами

```yaml
strategy:
  matrix:
    include:
      - service: bot
        dockerfile: Dockerfile.bot
        context: .
      - service: api
        dockerfile: Dockerfile.api
        context: .
      - service: frontend
        dockerfile: Dockerfile.frontend
        context: ./frontend
```

## Permissions и Secrets

### GITHUB_TOKEN

Автоматически создается для каждого workflow run. Используется для:
- Публикации в ghcr.io
- Создания releases
- Комментирования PR

```yaml
jobs:
  build:
    permissions:
      contents: read
      packages: write
    steps:
      - uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
```

### Secrets

Защищенные переменные (Settings → Secrets and variables → Actions):
- API ключи
- SSH ключи
- Токены доступа

```yaml
steps:
  - name: Deploy
    env:
      SSH_KEY: ${{ secrets.SSH_KEY }}
    run: ./deploy.sh
```

## Кэширование

Ускорение сборки через кэширование зависимостей.

### Кэш npm/pnpm

```yaml
- uses: actions/cache@v4
  with:
    path: ~/.pnpm-store
    key: ${{ runner.os }}-pnpm-${{ hashFiles('**/pnpm-lock.yaml') }}
    restore-keys: |
      ${{ runner.os }}-pnpm-
```

### Кэш Docker layers

```yaml
- uses: docker/setup-buildx-action@v3
- uses: docker/build-push-action@v5
  with:
    cache-from: type=gha
    cache-to: type=gha,mode=max
```

## Пример полного workflow

```yaml
name: Build and Publish

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write

    strategy:
      matrix:
        service: [bot, api, frontend]

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Log in to GitHub Container Registry
        if: github.event_name != 'pull_request'
        uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          context: .
          file: Dockerfile.${{ matrix.service }}
          push: ${{ github.event_name != 'pull_request' }}
          tags: |
            ghcr.io/${{ github.repository_owner }}/my-${{ matrix.service }}:latest
            ghcr.io/${{ github.repository_owner }}/my-${{ matrix.service }}:${{ github.sha }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
```

## Мониторинг и отладка

### Просмотр логов

1. Перейти в Actions → выбрать workflow run
2. Кликнуть на job → раскрыть step
3. Полные логи доступны в UI

### Отладка через SSH

Для сложных проблем можно подключиться к runner:

```yaml
- name: Setup tmate session
  uses: mxschmitt/action-tmate@v3
```

### Статус badges

Добавить в README.md:

```markdown
![Build Status](https://github.com/USER/REPO/actions/workflows/build.yml/badge.svg)
```

## Best Practices

1. **Используйте конкретные версии actions**: `actions/checkout@v4` вместо `@latest`
2. **Кэшируйте зависимости**: ускоряет сборку в 2-5 раз
3. **Используйте matrix для параллелизации**: экономит время
4. **Не храните секреты в коде**: только через GitHub Secrets
5. **Проверяйте PR перед мёрджем**: включите branch protection
6. **Ограничивайте permissions**: principle of least privilege

## Ресурсы

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [GitHub Actions Marketplace](https://github.com/marketplace?type=actions)
- [Working with GitHub Container Registry](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry)
- [Workflow syntax](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions)
