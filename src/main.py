"""Точка входа в приложение"""
import asyncio
from src.config import Config
from src.bot import Bot
from src.handler import MessageHandler
from src.llm_client import LLMClient


async def main() -> None:
    """Главная функция запуска бота"""
    # Загрузка конфигурации
    config = Config()

    # Инициализация бота
    bot = Bot(config)

    # Инициализация LLM клиента
    llm_client = LLMClient(config)

    # Инициализация обработчиков
    handler = MessageHandler(llm_client)
    bot.dp.include_router(handler.router)

    # Запуск бота
    print("Бот запущен...")
    await bot.start()


if __name__ == "__main__":
    asyncio.run(main())
