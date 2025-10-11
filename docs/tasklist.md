# План разработки LLM-ассистента

## 📊 Прогресс

| Итерация | Задача | Статус | Дата |
|----------|--------|--------|------|
| 1 | Инициализация и конфигурация | 🟢 Завершено | 2025-10-10 |
| 2 | Базовый Telegram бот | 🟢 Завершено | 2025-10-10 |
| 3 | Интеграция с LLM | 🟢 Завершено | 2025-10-10 |
| 4 | История диалогов с /clear | 🟢 Завершено | 2025-10-11 |
| 5 | Логгирование и обработка ошибок | 🟢 Завершено | 2025-10-11 |
| 6 | Команда /role (TDD) | 🟢 Завершено | 2025-10-11 |
| 7 | Системный промпт из файла | 🟢 Завершено | 2025-10-11 |

**Легенда**: 🔵 Не начато | 🟡 В процессе | 🟢 Завершено

---

## Итерация 1: Инициализация и конфигурация

**Цель**: Создать структуру проекта и реализовать конфигурацию

### Инициализация
- [x] Создать директории `src/` и `docs/`
- [x] Инициализировать проект: `uv init --python 3.11`
- [x] Добавить зависимости: `uv add aiogram openai python-dotenv structlog`
- [x] Создать директорию `logs/`
- [x] Создать `.gitignore` с записями `.env`, `__pycache__`, `.venv/`, `logs/`
- [x] Создать `Makefile` с командой `run` для запуска бота
- [x] Создать `README.md` с описанием проекта

### Конфигурация
- [x] Создать файл `src/config.py` с классом `Config`
- [x] Реализовать `Config.__init__()` с вызовом `load_dotenv()`
- [x] Загрузить `TELEGRAM_BOT_TOKEN` через `os.getenv()` с проверкой на None
- [x] Загрузить `OPENAI_API_KEY` через `os.getenv()` с проверкой на None
- [x] Загрузить `SYSTEM_PROMPT` через `os.getenv()` с проверкой на None
- [x] Загрузить `OPENAI_BASE_URL` с дефолтом "https://openrouter.ai/api/v1"
- [x] Загрузить `OPENAI_MODEL` с дефолтом "openai/gpt-4"
- [x] Загрузить `LOG_LEVEL` с дефолтом "INFO"
- [x] Загрузить `LOG_FILE_PATH` с дефолтом "logs/"
- [x] Загрузить `MAX_CONTEXT_MESSAGES` с дефолтом 0
- [x] Создать `.env.example` с примерами всех переменных

**Тест**: Выполнить `uv sync` без ошибок, запустить `uv run python -c "from src.config import Config; c = Config(); print(vars(c))"` и проверить вывод параметров

---

## Итерация 2: Базовый Telegram бот

**Цель**: Бот отвечает "Hello, {username}!" на любое сообщение

- [x] Создать файл `src/bot.py` с классом `Bot`
- [x] Реализовать `Bot.__init__()` с инициализацией `aiogram.Bot` и `Dispatcher`
- [x] Создать файл `src/handler.py` с классом `MessageHandler`
- [x] Реализовать обработчик команды `/start` с ответом "Привет! Я LLM-ассистент"
- [x] Реализовать обработчик текстовых сообщений с ответом "Hello, {username}!"
- [x] Создать файл `src/main.py` с запуском бота через `dp.start_polling()`
- [x] Добавить `src/__init__.py` (пустой файл)

**Тест**: Запустить `uv run python -m src.main`, отправить `/start` и текст, получить ответы

---

## Итерация 3: Интеграция с LLM

**Цель**: Бот отправляет сообщения в LLM и возвращает ответ (без истории)

- [x] Создать файл `src/llm_client.py` с классом `LLMClient`
- [x] Инициализировать `AsyncOpenAI` с `base_url="https://openrouter.ai/api/v1"`
- [x] Реализовать метод `async def generate_response(message: str) -> str`
- [x] Вызвать `client.chat.completions.create()` с model и messages
- [x] Вернуть `response.choices[0].message.content`
- [x] Создать экземпляр `LLMClient` в `MessageHandler`
- [x] Заменить "Hello, {username}!" на вызов `await llm_client.generate_response()`

**Тест**: Отправить "Напиши стих про кота", получить ответ от LLM

---

## Итерация 4: История диалогов с /clear

**Цель**: Бот поддерживает контекст диалога и позволяет его очистить

### История диалогов
- [x] Создать файл `src/dialog_manager.py` с классом `DialogManager`
- [x] Создать атрибут `dialogs: dict[int, list[dict]]` для хранения историй
- [x] Реализовать метод `get_history(user_id: int) -> list[dict]`
- [x] Добавить системный промпт при первом обращении пользователя
- [x] Реализовать метод `add_message(user_id: int, role: str, content: str)`
- [x] Создать экземпляр `DialogManager` в `MessageHandler`
- [x] Изменить `LLMClient.generate_response()` на прием `messages: list[dict]`
- [x] Передавать полную историю из DialogManager в LLMClient

### Команда /clear
- [x] Реализовать метод `clear_history(user_id: int)` в `DialogManager`
- [x] Добавить обработчик команды `/clear` в `MessageHandler`
- [x] Вызвать `dialog_manager.clear_history(user_id)`
- [x] Отправить ответ "История диалога очищена"

**Тест**: Сказать "Меня зовут Иван", затем "Как меня зовут?" (должен ответить "Иван"), отправить `/clear`, снова спросить - бот не должен помнить

---

## Итерация 5: Логгирование и обработка ошибок

**Цель**: Полное логгирование работы и правильная обработка ошибок

- [x] Настроить `structlog` в `main.py` с уровнем из Config
- [x] Настроить вывод логов в консоль и файл (LOG_FILE_PATH)
- [x] Добавить лог `logger.info("bot_started")` при запуске
- [x] Добавить лог `logger.info("message_received", user_id=..., text=...)` при получении
- [x] Добавить лог `logger.info("llm_request", model=..., messages=...)` перед запросом
- [x] Добавить лог `logger.info("llm_response", length=...)` после ответа
- [x] Обернуть вызов LLM в try/except с `logger.error("llm_error", exc_info=True)`
- [x] Отправить "Произошла ошибка, попробуйте позже" при ошибке

**Тест**: Запустить бота, проверить JSON логи в консоли и файле, ввести неверный API ключ - получить ошибку

---

## Итерация 6: Команда /role (TDD)

**Цель**: Реализовать команду `/role` для отображения роли и возможностей бота (подход TDD)

**Методология**: Red-Green-Refactor

### 🔴 RED: Тесты (failing tests)

#### Тесты для Config
- [x] Написать тест `test_config_loads_bot_role_name_from_env`
- [x] Написать тест `test_config_loads_bot_role_description_from_env`
- [x] Написать тест `test_config_has_default_bot_role_values`
- [x] Запустить тесты → убедиться что падают (атрибуты не существуют)

#### Тесты для MessageHandler (команда /role)
- [x] Написать тест `test_role_command_sends_bot_role_info`
- [x] Написать тест `test_role_command_includes_role_name`
- [x] Написать тест `test_role_command_includes_role_description`
- [x] Запустить тесты → убедиться что падают (обработчик не существует)

**Остановка**: Подтвердить failing тесты перед реализацией

### 🟢 GREEN: Минимальная реализация

#### Config: добавить параметры роли
- [x] Добавить `BOT_ROLE_NAME` в класс Config с дефолтом "ИИ-ассистент"
- [x] Добавить `BOT_ROLE_DESCRIPTION` в класс Config с дефолтом "Помогаю отвечать на вопросы"
- [x] Загрузить из `.env` через `os.getenv()` с дефолтами
- [x] Запустить тесты Config → убедиться что проходят ✅

#### MessageHandler: реализовать обработчик /role
- [x] Создать async метод `handle_role_command(message: Message)`
- [x] Сформировать текст с `config.BOT_ROLE_NAME` и `config.BOT_ROLE_DESCRIPTION`
- [x] Отправить сообщение пользователю через `message.answer()`
- [x] Зарегистрировать обработчик команды `/role` в роутере
- [x] Запустить все тесты → убедиться что проходят ✅

### ♻️ REFACTOR: Улучшение (если нужно)
- [x] Проверить форматирование текста команды `/role`
- [x] Добавить эмодзи для улучшения UX (опционально)
- [x] Запустить `make lint` → проверить качество кода
- [x] Запустить `make test-cov` → проверить coverage

### Обновление конфигурации
- [x] Обновить `.env.example` с новыми параметрами:
  - `BOT_ROLE_NAME=Консультант по выбору музыки 🎵`
  - `BOT_ROLE_DESCRIPTION=Помогаю найти музыку по настроению, рекомендую треки и составляю плейлисты`

**Тест**:
1. Запустить бота `make run`
2. Отправить `/role` → получить сообщение с названием роли и описанием
3. Проверить что отображается корректно
4. Запустить `make test` → все тесты проходят ✅

---

## Итерация 7: Системный промпт из файла

**Цель**: Перенести системный промпт из `.env` в отдельный файл (подход TDD)

**Методология**: Red-Green-Refactor

### 🔴 RED: Тесты (failing tests)

#### Тесты для Config
- [x] Написать тест `test_config_loads_system_prompt_from_file`
- [x] Написать тест `test_config_falls_back_to_env_prompt`
- [x] Написать тест `test_config_raises_error_when_no_prompt`
- [x] Написать тест `test_config_raises_error_when_prompt_file_not_found`
- [x] Запустить тесты → убедиться что падают

**Остановка**: Подтвердить failing тесты перед реализацией

### 🟢 GREEN: Минимальная реализация

#### Создать директорию и файл промпта
- [x] Создать директорию `prompts/`
- [x] Создать файл `prompts/music_consultant.txt` с системным промптом
- [x] Добавить `prompts/` в `.gitignore` (опционально, можно хранить в репо)

#### Config: загрузка промпта из файла
- [x] Добавить параметр `SYSTEM_PROMPT_FILE` в Config
- [x] Реализовать метод `_load_system_prompt()`:
  - Проверить наличие `SYSTEM_PROMPT_FILE`
  - Если есть - читать из файла
  - Иначе - использовать `SYSTEM_PROMPT` из env
  - Если ничего нет - выбросить ValueError
- [x] Вызвать `_load_system_prompt()` в `__init__()`
- [x] Запустить тесты → убедиться что проходят ✅

### ♻️ REFACTOR: Улучшение
- [x] Добавить обработку ошибок чтения файла (FileNotFoundError)
- [x] Добавить логирование загрузки промпта
- [x] Запустить `make lint` и `make test`

### Обновление конфигурации
- [x] Обновить `.env.example`:
  - Закомментировать `SYSTEM_PROMPT=...`
  - Добавить `SYSTEM_PROMPT_FILE=prompts/music_consultant.txt`
- [x] Создать пример промпта для музыкального консультанта

**Тест**:
1. Создать файл `prompts/music_consultant.txt` с промптом
2. Установить `SYSTEM_PROMPT_FILE` в `.env`
3. Запустить бота → проверить что промпт загружен из файла
4. Отправить сообщение → убедиться что бот ведет себя как консультант по музыке

---

**Справка**: См. [vision.md](./vision.md) и [conventions.md](./conventions.md)
