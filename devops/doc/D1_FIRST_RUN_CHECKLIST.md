# Спринт D1: Чеклист первого запуска

## Предварительная проверка

Перед первым push в main, убедитесь что все файлы на месте:

```bash
# Проверить наличие workflow
ls -la .github/workflows/build.yml

# Проверить docker-compose файлы
ls -la docker-compose.yml docker-compose.registry.yml

# Проверить документацию
ls -la devops/doc/guides/github-*.md
ls -la DOCKER_QUICKSTART.md
```

## Шаг 1: Настройка GitHub Permissions

**Важно**: Это нужно сделать ПЕРЕД первым push!

1. Перейти в репозиторий: https://github.com/natapage/telegram-bot
2. Settings → Actions → General
3. Прокрутить до "Workflow permissions"
4. ✅ Выбрать: **Read and write permissions**
5. Нажать **Save**

## Шаг 2: Первый Push

```bash
# Убедиться что все изменения закоммичены
git status

# Добавить все новые файлы
git add .github/ docker-compose.registry.yml DOCKER_QUICKSTART.md
git add devops/doc/guides/ devops/doc/plans/
git add SPRINT_D1_SUMMARY.md

# Коммит
git commit -m "feat(devops): Add GitHub Actions workflow for Docker image builds

- Add .github/workflows/build.yml with matrix strategy
- Add docker-compose.registry.yml for ghcr.io images
- Add Makefile commands for registry operations
- Add comprehensive documentation (GitHub Actions intro, registry setup)
- Add DOCKER_QUICKSTART.md for quick reference
- Update README.md with build badge and registry instructions
- Update devops roadmap with D1 status

Sprint D1: Build & Publish"

# Push в main
git push origin main
```

## Шаг 3: Мониторинг первой сборки

1. **Открыть GitHub Actions**:
   - Перейти: https://github.com/natapage/telegram-bot/actions
   - Найти workflow run: "Build and Publish Docker Images"

2. **Проверить статус jobs**:
   - build (bot) - должен быть зеленый ✅
   - build (api) - должен быть зеленый ✅
   - build (frontend) - должен быть зеленый ✅

3. **Просмотр логов** (если нужно):
   - Кликнуть на job
   - Раскрыть steps
   - Проверить "Build and push Docker image"

**Ожидаемое время**: 5-10 минут для первой сборки

## Шаг 4: Проверка опубликованных образов

1. **Найти пакеты**:
   - Способ 1: Перейти на https://github.com/natapage?tab=packages
   - Способ 2: В репозитории → справа → Packages

2. **Должны быть 3 пакета**:
   - telegram-bot-bot
   - telegram-bot-api
   - telegram-bot-frontend

3. **Проверить теги**:
   - Открыть каждый пакет
   - Должны быть теги: `latest` и `sha-XXXXXX`

## Шаг 5: Изменить visibility на Public

**Для каждого из 3 пакетов** (bot, api, frontend):

1. Открыть страницу пакета
2. Кликнуть **Package settings** (справа)
3. Прокрутить до "Danger Zone"
4. Найти **Change package visibility**
5. Кликнуть **Change visibility**
6. В модальном окне:
   - Выбрать **Public**
   - Ввести название пакета для подтверждения
   - Нажать "I understand the consequences, change package visibility"

## Шаг 6: Локальное тестирование

### 6.1. Pull образов

```bash
# Pull всех образов
docker pull ghcr.io/natapage/telegram-bot-bot:latest
docker pull ghcr.io/natapage/telegram-bot-api:latest
docker pull ghcr.io/natapage/telegram-bot-frontend:latest

# Или через make
make docker-pull
```

**Ожидаемый результат**: Образы загружаются без ошибок

### 6.2. Проверка образов

```bash
# Посмотреть загруженные образы
docker images | grep ghcr.io/natapage/telegram-bot

# Должны видеть 3 образа с тегом latest
```

### 6.3. Запуск через registry

```bash
# Убедиться что .env файл существует
ls -la .env

# Если нет - создать
cp .env.example .env
# Отредактировать и добавить токены

# Остановить локальные контейнеры если запущены
make docker-down

# Запустить с registry образами
make docker-up-registry

# Подождать 10-20 секунд для старта

# Проверить статус
make docker-status-registry
```

**Ожидаемый результат**: Все 3 контейнера в статусе "Up"

### 6.4. Проверка работоспособности

```bash
# API health check
curl http://localhost:8000/health
# Должен вернуть: {"status":"ok"}

# Frontend
curl http://localhost:3001
# Должен вернуть HTML

# Или открыть в браузере:
# http://localhost:8000/docs
# http://localhost:3001
```

### 6.5. Проверка логов

```bash
# Логи всех сервисов
make docker-logs-registry

# Или конкретного сервиса
docker-compose -f docker-compose.registry.yml logs bot
docker-compose -f docker-compose.registry.yml logs api
docker-compose -f docker-compose.registry.yml logs frontend
```

**Ожидается**: Нормальные логи запуска без ERROR

## Шаг 7: Тестирование PR workflow

1. **Создать тестовую ветку**:
   ```bash
   git checkout -b test/workflow-check
   ```

2. **Сделать небольшое изменение**:
   ```bash
   echo "# Test" >> test.md
   git add test.md
   git commit -m "test: Check workflow on PR"
   git push origin test/workflow-check
   ```

3. **Создать Pull Request**:
   - Перейти на GitHub
   - Создать PR из test/workflow-check в main
   - Проверить что workflow запустился
   - Проверить что образы собираются (но НЕ публикуются)

4. **Закрыть PR** (не мёржить):
   - Это был просто тест
   - Удалить ветку после закрытия

## Шаг 8: Документирование результатов

Обновить `SPRINT_D1_SUMMARY.md` с результатами:

```bash
# Открыть файл
nano SPRINT_D1_SUMMARY.md

# Заполнить секцию "Ожидаемые результаты тестирования":
# - Время первой сборки
# - Время с кэшем
# - Размер образов
# - Проблемы (если были)
```

## Troubleshooting

### ❌ Ошибка: Permission denied

**Проблема**: Workflow не может публиковать пакеты

**Решение**:
1. Проверить Workflow permissions (Шаг 1)
2. Убедиться что "Read and write permissions" выбрано
3. Перезапустить workflow

### ❌ Образы не public

**Проблема**: `docker pull` требует авторизацию

**Решение**:
- Следовать Шаг 5
- Изменить visibility каждого пакета на Public
- Это нужно сделать только один раз

### ❌ Ошибка сборки frontend

**Проблема**: Неправильный контекст или путь к Dockerfile

**Решение**:
- Проверить что context: ./frontend
- Проверить что file: Dockerfile.frontend
- Path к Dockerfile должен быть относительно workspace root

### ❌ Порт уже занят

**Проблема**: 8000 или 3001 порты заняты

**Решение**:
```bash
# Остановить локальные контейнеры
make docker-down

# Проверить что порты свободны
lsof -i :8000
lsof -i :3001

# Запустить registry версию
make docker-up-registry
```

## Чеклист завершения

После успешного прохождения всех шагов:

- [ ] Workflow permissions настроены
- [ ] Первый push в main выполнен
- [ ] Все 3 образа успешно собраны в CI
- [ ] Пакеты опубликованы в ghcr.io
- [ ] Visibility изменен на Public для всех пакетов
- [ ] Образы успешно pull'ятся без авторизации
- [ ] Сервисы запускаются через docker-compose.registry.yml
- [ ] API отвечает на /health
- [ ] Frontend отображается
- [ ] PR workflow протестирован
- [ ] Результаты задокументированы

## Готово!

После завершения чеклиста:

1. **Обновить статус спринта**:
   ```bash
   # В devops/doc/devops-roadmap.md
   # Изменить D1: 🚧 In Progress → ✅ Completed
   ```

2. **Создать финальный summary**:
   - Обновить SPRINT_D1_SUMMARY.md с результатами
   - Добавить секцию "Результаты тестирования"

3. **Коммит и push**:
   ```bash
   git add SPRINT_D1_SUMMARY.md devops/doc/devops-roadmap.md
   git commit -m "docs(devops): Complete Sprint D1 - Build & Publish"
   git push origin main
   ```

## Следующие шаги

**Спринт D2: Manual Deploy**
- Получить доступ к серверу (SSH ключ)
- Создать инструкцию по ручному развертыванию
- Развернуть проект на сервер
- Задокументировать процесс и проблемы

---

**Удачи!** 🚀
