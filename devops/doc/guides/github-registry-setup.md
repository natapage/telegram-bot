# Настройка GitHub Container Registry

## Обзор

Пошаговая инструкция по настройке публикации Docker образов в GitHub Container Registry (ghcr.io) для проекта telegram-bot.

## Предварительные требования

- Репозиторий на GitHub: `natapage/telegram-bot`
- Права администратора репозитория
- Созданный workflow файл `.github/workflows/build.yml`

## Шаг 1: Настройка Workflow Permissions

GitHub Actions требует права на публикацию пакетов.

### 1.1. Открыть настройки репозитория

1. Перейти в репозиторий: https://github.com/natapage/telegram-bot
2. Кликнуть **Settings** (в верхнем меню)
3. В левом меню выбрать **Actions** → **General**

### 1.2. Настроить Workflow permissions

Прокрутить вниз до секции **Workflow permissions**:

**Выбрать**: ✅ **Read and write permissions**

Это дает workflow права на:
- Чтение кода (checkout)
- Публикацию пакетов (push to ghcr.io)
- Создание releases

**Сохранить**: кнопка **Save** внизу страницы

### Скриншот настройки

```
Workflow permissions
────────────────────────────────────────────────
Choose the default permissions granted to the GITHUB_TOKEN when running workflows in this repository.

○ Read repository contents and packages permissions
● Read and write permissions

This sets the default permissions granted to GITHUB_TOKEN. The GITHUB_TOKEN is used by
workflows to authenticate in the repository. You can override these settings for specific
workflows.

□ Allow GitHub Actions to create and approve pull requests
  This controls whether GitHub Actions can create pull requests or submit approving pull
  request reviews.
```

## Шаг 2: Первая публикация образов

### 2.1. Запуск workflow

После push в ветку `main`, workflow автоматически запустится:

```bash
git add .
git commit -m "Add GitHub Actions workflow"
git push origin main
```

### 2.2. Мониторинг выполнения

1. Перейти во вкладку **Actions** репозитория
2. Выбрать workflow run (последний в списке)
3. Проверить статус jobs:
   - ✅ build (bot)
   - ✅ build (api)
   - ✅ build (frontend)

### 2.3. Просмотр логов

Кликнуть на job → раскрыть steps:
- "Log in to GitHub Container Registry" - авторизация
- "Build and push Docker image" - сборка и публикация
- Проверить что push прошел успешно

## Шаг 3: Настройка публичного доступа

По умолчанию пакеты создаются как **private** (приватные). Нужно изменить на **public**.

### 3.1. Найти опубликованные пакеты

**Способ 1**: Через профиль
1. Перейти на главную страницу профиля: https://github.com/natapage
2. Кликнуть вкладку **Packages**

**Способ 2**: Через репозиторий
1. Перейти в репозиторий: https://github.com/natapage/telegram-bot
2. Справа в боковой панели найти секцию **Packages**
3. Кликнуть на пакет (например, `telegram-bot-bot`)

### 3.2. Изменить видимость на Public

Для каждого пакета (bot, api, frontend):

1. Открыть страницу пакета
2. Кликнуть **Package settings** (справа)
3. Прокрутить вниз до секции **Danger Zone**
4. Найти **Change package visibility**
5. Кликнуть **Change visibility**
6. В модальном окне:
   - Выбрать **Public**
   - Ввести название пакета для подтверждения
   - Кликнуть **I understand the consequences, change package visibility**

### 3.3. Проверка публичного доступа

После изменения видимости, попробовать pull без авторизации:

```bash
# Должно работать без docker login
docker pull ghcr.io/natapage/telegram-bot-bot:latest
docker pull ghcr.io/natapage/telegram-bot-api:latest
docker pull ghcr.io/natapage/telegram-bot-frontend:latest
```

## Шаг 4: Связь пакета с репозиторием

Рекомендуется явно связать пакет с репозиторием.

### 4.1. Добавить связь

1. Открыть страницу пакета
2. Справа в боковой панели найти **Connect repository**
3. Выбрать `natapage/telegram-bot`
4. Кликнуть **Connect**

**Преимущества**:
- Пакет отображается в репозитории
- Упрощенная навигация
- Автоматическое связывание с releases

## Шаг 5: Проверка работоспособности

### 5.1. Проверить список образов

```bash
# Список тегов для bot
curl https://ghcr.io/v2/natapage/telegram-bot-bot/tags/list

# Ожидаемый ответ
{
  "name": "natapage/telegram-bot-bot",
  "tags": ["latest", "sha-abc123"]
}
```

### 5.2. Pull образов локально

```bash
# Pull всех образов
docker pull ghcr.io/natapage/telegram-bot-bot:latest
docker pull ghcr.io/natapage/telegram-bot-api:latest
docker pull ghcr.io/natapage/telegram-bot-frontend:latest

# Проверить что образы загружены
docker images | grep ghcr.io/natapage/telegram-bot
```

### 5.3. Запуск через docker-compose

```bash
# Использовать docker-compose.registry.yml
docker-compose -f docker-compose.registry.yml up -d

# Проверить статус
docker-compose -f docker-compose.registry.yml ps

# Проверить логи
docker-compose -f docker-compose.registry.yml logs -f
```

## Как работает автоматическая публикация

### При push в main

1. **Trigger**: Коммит в `main` запускает workflow
2. **Checkout**: Клонирование кода
3. **Docker Buildx**: Настройка builder с кэшированием
4. **Login**: Авторизация в ghcr.io через `GITHUB_TOKEN`
5. **Build**: Сборка образа для каждого сервиса (параллельно)
6. **Tag**: Применение тегов `latest` и `sha-XXXXXX`
7. **Push**: Публикация образов в registry
8. **Cache**: Сохранение Docker layers для следующей сборки

### При Pull Request

Workflow также запускается, но:
- **Без публикации**: только проверка что образ собирается
- **Быстрее**: используется кэш от предыдущих сборок
- **Безопасно**: не загрязняет registry тестовыми образами

## Адреса опубликованных образов

После настройки, образы доступны по адресам:

```
ghcr.io/natapage/telegram-bot-bot:latest
ghcr.io/natapage/telegram-bot-bot:sha-XXXXXX

ghcr.io/natapage/telegram-bot-api:latest
ghcr.io/natapage/telegram-bot-api:sha-XXXXXX

ghcr.io/natapage/telegram-bot-frontend:latest
ghcr.io/natapage/telegram-bot-frontend:sha-XXXXXX
```

### Теги

- **latest**: Последняя версия из main ветки (обновляется при каждом push)
- **sha-XXXXXX**: Конкретный коммит (неизменяемый, для воспроизводимости)

## Использование в production

### Рекомендации по тегам

**Development**:
```yaml
image: ghcr.io/natapage/telegram-bot-api:latest
```
Всегда последняя версия, автоматические обновления.

**Production**:
```yaml
image: ghcr.io/natapage/telegram-bot-api:sha-abc123f
```
Фиксированная версия, воспроизводимость, стабильность.

### Pull всегда свежей версии

```bash
# Остановить сервисы
docker-compose -f docker-compose.registry.yml down

# Pull обновлений
docker-compose -f docker-compose.registry.yml pull

# Запустить с новыми образами
docker-compose -f docker-compose.registry.yml up -d
```

## Troubleshooting

### Ошибка: Permission denied

**Проблема**: Workflow не может публиковать пакеты

**Решение**:
1. Проверить Workflow permissions (Шаг 1.2)
2. Убедиться что выбрано "Read and write permissions"

### Ошибка: Package already exists

**Проблема**: Пакет создан вручную и конфликтует

**Решение**:
1. Удалить старый пакет через UI
2. Запустить workflow заново

### Образы остаются private

**Проблема**: После публикации образы недоступны без авторизации

**Решение**:
1. Следовать Шаг 3: изменить visibility на Public
2. Это нужно сделать только один раз для каждого пакета

### Pull выдает 404

**Проблема**: `docker pull ghcr.io/natapage/telegram-bot-bot:latest` возвращает 404

**Варианты**:
1. Пакет еще private → изменить на public (Шаг 3)
2. Опечатка в имени пакета → проверить точное имя в Packages
3. Пакет не был опубликован → проверить логи workflow

## Дополнительные возможности

### Автоматическая очистка старых образов

GitHub автоматически удаляет старые untagged образы через 14 дней.

Для более агрессивной очистки:
1. Package settings → Manage versions
2. Выбрать старые версии
3. Delete versions

### Webhooks

Можно настроить уведомления при публикации:
1. Package settings → Webhooks
2. Add webhook
3. Указать URL для уведомлений

## Готово!

После выполнения всех шагов:
- ✅ Автоматическая сборка при push в main
- ✅ Публикация в ghcr.io
- ✅ Публичный доступ к образам
- ✅ Кэширование для ускорения сборки
- ✅ Теги latest и sha для гибкости

Образы готовы к использованию на любом сервере с Docker!

## Следующие шаги

- **Спринт D2**: Ручное развертывание на сервер
- **Спринт D3**: Автоматический деплой через GitHub Actions
