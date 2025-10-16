"""Точка входа в приложение"""

import asyncio
from pathlib import Path
from typing import cast

import structlog

from src.bot import Bot
from src.config import Config
from src.database import Database
from src.dialog_manager import DialogManager
from src.handler import MessageHandler
from src.llm_client import LLMClient
from src.message_repository import MessageRepository


def setup_logging(config: Config) -> structlog.BoundLogger:
    """Настройка structlog

    Args:
        config: Конфигурация приложения

    Returns:
        Настроенный logger
    """
    # Создать директорию для логов если не существует
    Path(config.LOG_FILE_PATH).mkdir(parents=True, exist_ok=True)

    # Настройка процессоров
    structlog.configure(
        processors=[
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.add_log_level,
            structlog.processors.JSONRenderer(),
        ],
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True,
    )

    return cast("structlog.BoundLogger", structlog.get_logger())


async def main() -> None:
    """Главная функция запуска бота"""
    # Загрузка конфигурации
    config = Config()

    # Настройка логирования
    logger = setup_logging(config)

    # Инициализация бота
    bot = Bot(config)

    # Инициализация LLM клиента
    llm_client = LLMClient(config, logger)

    # Инициализация базы данных и репозитория
    database = Database(config)
    message_repository = MessageRepository(database)

    # Инициализация менеджера диалогов
    dialog_manager = DialogManager(config, message_repository)

    # Инициализация обработчиков
    handler = MessageHandler(llm_client, dialog_manager, logger)
    bot.dp.include_router(handler.router)

    # Запуск бота
    logger.info("bot_started", model=config.OPENAI_MODEL)
    print("Бот запущен...")
    await bot.start()


if __name__ == "__main__":
    asyncio.run(main())
