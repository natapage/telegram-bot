"""Entrypoint для запуска API сервера дашборда статистики"""

import structlog
import uvicorn

# Настройка логирования
structlog.configure(
    processors=[
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.dev.ConsoleRenderer(),
    ],
    wrapper_class=structlog.make_filtering_bound_logger(structlog.INFO),
    context_class=dict,
    logger_factory=structlog.PrintLoggerFactory(),
    cache_logger_on_first_use=False,
)

logger = structlog.get_logger()


def main() -> None:
    """Запустить API сервер"""
    logger.info(
        "starting_api_server",
        host="0.0.0.0",
        port=8000,
        docs_url="http://localhost:8000/docs",
    )

    uvicorn.run(
        "src.api.app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Auto-reload для разработки
        log_level="info",
    )


if __name__ == "__main__":
    main()
