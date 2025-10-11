"""Точка входа в приложение"""
import asyncio
import structlog
from pathlib import Path
from src.config import Config
from src.bot import Bot
from src.handler import MessageHandler
from src.llm_client import LLMClient
from src.dialog_manager import DialogManager


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
            structlog.processors.JSONRenderer()
        ],
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True,
    )

    return structlog.get_logger()


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

    # Инициализация менеджера диалогов
    dialog_manager = DialogManager(config)

    # Инициализация обработчиков
    handler = MessageHandler(llm_client, dialog_manager, logger)
    bot.dp.include_router(handler.router)

    # Запуск бота
    logger.info("bot_started", model=config.OPENAI_MODEL)
    print("Бот запущен...")
    await bot.start()


if __name__ == "__main__":
    asyncio.run(main())
