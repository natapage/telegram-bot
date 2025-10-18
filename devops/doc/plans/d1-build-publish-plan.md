# План Спринта D1: Build & Publish

**Дата начала**: 18 октября 2025
**Статус**: 🚧 В работе

## Цель

Автоматизировать сборку и публикацию Docker образов в GitHub Container Registry (ghcr.io) для упрощения развертывания и подготовки к следующим спринтам (D2: Manual Deploy, D3: Auto Deploy).

## Контекст

**Спринт D0** завершен:
- ✅ Созданы Dockerfile для bot, api, frontend
- ✅ Настроен docker-compose для локального запуска
- ✅ Все сервисы успешно работают локально

**Текущие ограничения**:
- Образы собираются только локально
- Нет автоматизации сборки
- Невозможно развернуть на сервере без сборки
- Отсутствует версионирование образов

**Что даст D1**:
- Автоматическая сборка при push в main
- Публичные образы в ghcr.io
- Готовность к быстрому развертыванию
- CI/CD pipeline (базовый)

## Архитектура решения

### GitHub Actions Workflow

```
Push в main → Trigger workflow → Build (matrix: bot, api, frontend) → Push to ghcr.io
                                     ↓
                              Docker BuildKit + Cache
                                     ↓
                              Tags: latest, sha-XXXXXX
```

### Структура образов

```
ghcr.io/natapage/telegram-bot-bot:latest
ghcr.io/natapage/telegram-bot-bot:sha-abc123f

ghcr.io/natapage/telegram-bot-api:latest
ghcr.io/natapage/telegram-bot-api:sha-abc123f

ghcr.io/natapage/telegram-bot-frontend:latest
ghcr.io/natapage/telegram-bot-frontend:sha-abc123f
```

## Компоненты

### 1. GitHub Actions Workflow

**Файл**: `.github/workflows/build.yml`

**Ключевые решения**:

1. **Trigger**: `push` в `main` + `pull_request`
   - Push → сборка и публикация
   - PR → только сборка (проверка)

2. **Matrix strategy**:
   ```yaml
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

   Параллельная сборка 3 образов → экономия времени в 3 раза.

3. **Кэширование**:
   ```yaml
   cache-from: type=gha
   cache-to: type=gha,mode=max
   ```

   GitHub Actions Cache → последующие сборки в 2-5 раз быстрее.

4. **Тегирование**:
   - `latest` - для development и staging
   - `sha-XXXXXX` - для production (воспроизводимость)

5. **Permissions**:
   ```yaml
   permissions:
     contents: read
     packages: write
   ```

   Минимальные права для безопасности.

### 2. Docker Compose для Registry

**Файл**: `docker-compose.registry.yml`

**Отличия от docker-compose.yml**:

| Аспект | docker-compose.yml | docker-compose.registry.yml |
|--------|-------------------|----------------------------|
| Сборка | `build: ...` | `image: ghcr.io/...` |
| Использование | Разработка | Production |
| Скорость | ~90-120 сек | ~10-30 сек |
| Требует | Исходники | Только .env |

**Зачем два файла**:
- Разработчики используют локальную сборку (видят изменения сразу)
- Production использует registry (стабильность, скорость)
- Явное разделение → меньше ошибок

### 3. Makefile команды

**Новые команды**:

```makefile
# Registry образы
docker-pull           # Pull образов из ghcr.io
docker-up-registry    # Запуск с registry образами
docker-down-registry  # Остановка
docker-logs-registry  # Логи
docker-status-registry # Статус
```

**Организация**:
- Группа "локальная сборка" - существующие команды
- Группа "registry образы" - новые команды
- Понятные префиксы → легко найти нужную команду

### 4. Документация

#### github-actions-intro.md

**Содержание**:
- Что такое GitHub Actions (для новичков)
- Основные концепции: workflow, jobs, steps, actions
- Triggers и их использование
- Работа с Pull Requests
- GitHub Container Registry
- Public vs Private образы
- Matrix strategy
- Best practices

**Цель**: Понимание основ перед настройкой.

#### github-registry-setup.md

**Содержание**:
- Пошаговая инструкция настройки
- Настройка Workflow permissions
- Первая публикация образов
- Изменение visibility на Public
- Проверка работоспособности
- Troubleshooting

**Цель**: Пошаговый гайд "сделай и работает".

#### DOCKER_QUICKSTART.md

**Содержание**:
- Два способа запуска (локальный vs registry)
- Когда использовать каждый
- Команды для обоих вариантов
- Сравнительная таблица
- Best practices
- Troubleshooting

**Цель**: Быстрый выбор правильного подхода.

## Технические решения

### Почему GitHub Container Registry?

**Альтернативы**: Docker Hub, AWS ECR, Google GCR

**Выбор ghcr.io**:
- ✅ Бесплатно для публичных образов
- ✅ Интеграция с GitHub (один аккаунт)
- ✅ Автоматическая авторизация через GITHUB_TOKEN
- ✅ Простота настройки
- ✅ Хорошая производительность

### Почему Matrix Strategy?

**Альтернатива**: 3 отдельных jobs

**Преимущества matrix**:
- Параллельное выполнение
- Меньше дублирования кода
- Легко добавить новый сервис
- Унифицированная логика

### Почему два docker-compose файла?

**Альтернатива**: Один файл с переменными окружения

**Преимущества двух файлов**:
- Явное разделение → меньше путаницы
- Разные use cases → разные файлы
- Простота понимания (один файл = один способ)
- Невозможно случайно смешать

### Стратегия тегирования

**latest**:
- Всегда последняя версия из main
- Удобно для development/staging
- Автоматические обновления

**sha-XXXXXX**:
- Привязка к конкретному коммиту
- Воспроизводимость
- Стабильность для production

**Не используем** (пока):
- Версионные теги (v1.0.0) - добавим позже
- Branch теги (develop-latest) - не нужно для MVP

## MVP подход

### Включено

✅ **Автоматическая сборка**:
- Push в main → автоматическая сборка
- Параллельная сборка 3 образов
- Кэширование для скорости

✅ **Публикация**:
- GitHub Container Registry
- Публичные образы (без авторизации для pull)
- Теги: latest, sha

✅ **Удобство использования**:
- Два способа запуска (local vs registry)
- Makefile команды
- Детальная документация

✅ **Проверка PR**:
- Сборка образов на PR
- Проверка что изменения собираются

### Не включено (для будущих спринтов)

❌ **Lint checks в CI**:
- Пока делаем вручную: `make lint`
- Добавим в будущем спринте

❌ **Unit/Integration тесты в CI**:
- Пока запускаем локально: `make test`
- Добавим позже

❌ **Security scanning**:
- Trivy, Snyk и т.д.
- Не критично для MVP

❌ **Multi-platform builds**:
- Пока только amd64 (Linux x86_64)
- Arm64 добавим если понадобится

❌ **Версионные теги**:
- v1.0.0, v1.0.1 и т.д.
- Добавим при необходимости

❌ **Уведомления**:
- Slack/Telegram уведомления о сборке
- Полезно, но не обязательно

## Этапы реализации

### Этап 1: Документация (основы)

- [x] Создать `github-actions-intro.md`
- [x] Создать `github-registry-setup.md`

### Этап 2: CI/CD

- [x] Создать `.github/workflows/build.yml`
- [ ] Протестировать workflow

### Этап 3: Docker Compose

- [x] Создать `docker-compose.registry.yml`
- [x] Добавить комментарии в `docker-compose.yml`

### Этап 4: Удобство использования

- [x] Обновить `Makefile` с registry командами
- [x] Создать `DOCKER_QUICKSTART.md`
- [x] Обновить `README.md` с badge и инструкциями

### Этап 5: Документация проекта

- [x] Создать детальный план (этот файл)
- [ ] Обновить `devops-roadmap.md`

### Этап 6: Тестирование

- [ ] Настроить Workflow permissions
- [ ] Push в main → проверка автосборки
- [ ] Изменить visibility образов на Public
- [ ] Pull образов локально
- [ ] Запустить через `docker-compose.registry.yml`
- [ ] Проверить все сервисы

## Команды для тестирования

### Локальная проверка workflow

```bash
# Установить act (для локального запуска GitHub Actions)
# https://github.com/nektos/act

# Запустить workflow локально
act push -j build
```

### После публикации

```bash
# Pull образов
docker pull ghcr.io/natapage/telegram-bot-bot:latest
docker pull ghcr.io/natapage/telegram-bot-api:latest
docker pull ghcr.io/natapage/telegram-bot-frontend:latest

# Проверить образы
docker images | grep telegram-bot

# Запустить через registry
make docker-up-registry

# Проверить логи
make docker-logs-registry

# Проверить что все работает
curl http://localhost:8000/health
curl http://localhost:3001
```

## Критерии успеха

✅ **Сборка**:
- [ ] Workflow успешно запускается при push в main
- [ ] Все 3 образа собираются параллельно
- [ ] Сборка завершается без ошибок

✅ **Публикация**:
- [ ] Образы публикуются в ghcr.io
- [ ] Образы имеют теги latest и sha
- [ ] Образы публичные (доступны без авторизации)

✅ **Использование**:
- [ ] `make docker-pull` успешно загружает образы
- [ ] `make docker-up-registry` запускает все сервисы
- [ ] Frontend доступен на http://localhost:3001
- [ ] API доступен на http://localhost:8000
- [ ] Bot запускается и готов к работе

✅ **Документация**:
- [ ] README.md обновлен с badge и инструкциями
- [ ] DOCKER_QUICKSTART.md создан
- [ ] Гайды по GitHub Actions созданы

## Следующие шаги (Спринт D2)

После завершения D1:

1. **Ручное развертывание на сервер**:
   - Получить доступ к серверу (SSH ключ)
   - Создать пошаговую инструкцию деплоя
   - Развернуть вручную, задокументировать проблемы

2. **Подготовка к автодеплою**:
   - Скрипт проверки работоспособности
   - Шаблон .env для production
   - Документация по настройке сервера

## Риски и митигация

### Риск: Образы не собираются в CI

**Вероятность**: Средняя
**Митигация**:
- Тестируем локально перед push
- Проверяем синтаксис YAML
- Используем проверенные actions из Marketplace

### Риск: Образы слишком большие

**Вероятность**: Низкая
**Митигация**:
- Используем slim базовые образы
- .dockerignore исключает ненужное
- Multi-stage builds добавим если нужно

### Риск: Медленная сборка в CI

**Вероятность**: Средняя
**Митигация**:
- Кэширование Docker layers (type=gha)
- Matrix strategy для параллелизации
- Последующие сборки в 2-5 раз быстрее

### Риск: Проблемы с permissions

**Вероятность**: Высокая (типичная проблема)
**Митигация**:
- Детальная документация настройки
- Пошаговые инструкции со скриншотами
- Секция Troubleshooting

## Ресурсы

### Файлы проекта

```
telegram-bot/
├── .github/
│   └── workflows/
│       └── build.yml                          # GitHub Actions workflow
├── devops/
│   └── doc/
│       ├── guides/
│       │   ├── github-actions-intro.md        # Введение в GitHub Actions
│       │   └── github-registry-setup.md       # Настройка ghcr.io
│       └── plans/
│           └── d1-build-publish-plan.md       # Этот файл
├── docker-compose.yml                          # Локальная сборка
├── docker-compose.registry.yml                 # Registry образы
├── DOCKER_QUICKSTART.md                        # Быстрая инструкция
├── Makefile                                    # Команды (обновлен)
└── README.md                                   # Главная документация (обновлен)
```

### Внешние ресурсы

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [GitHub Container Registry](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry)
- [Docker Build Push Action](https://github.com/docker/build-push-action)
- [Docker Metadata Action](https://github.com/docker/metadata-action)

## Оценка времени

- Документация: 2 часа ✅
- GitHub Actions workflow: 1 час ✅
- Docker Compose для registry: 30 минут ✅
- Makefile и README: 30 минут ✅
- Тестирование и отладка: 1-2 часа ⏳
- Документация результатов: 30 минут ⏳

**Итого**: ~5-6 часов

## Результаты

_Секция будет заполнена после завершения тестирования_

### Сборка

- Время первой сборки: ?
- Время с кэшем: ?
- Размер образов: ?

### Проблемы

_Будет заполнено при обнаружении_

### Улучшения

_Идеи для будущих спринтов_

---

**Статус**: 🚧 Реализация в процессе
**Следующий спринт**: D2 - Manual Deploy
