"""Сервис для обработки text-to-SQL запросов (admin mode)"""

import re

import structlog

from src.api.schemas import ChatRequest, ChatResponse
from src.api.session_manager import session_id_to_user_id
from src.config import Config
from src.database import Database
from src.llm_client import LLMClient

# Промпт для генерации SQL
TEXT_TO_SQL_PROMPT = """You are a SQL expert. Generate a SQL query for SQLite database.

Database Schema:
- users (id INTEGER PRIMARY KEY, created_at TEXT, is_deleted INTEGER)
- messages (id INTEGER PRIMARY KEY, user_id INTEGER, role TEXT, content TEXT, length INTEGER, created_at TEXT, is_deleted INTEGER)

Important rules:
- Only generate SELECT queries
- Do NOT use DROP, DELETE, UPDATE, INSERT, ALTER commands
- Use WHERE is_deleted = 0 to filter active records
- created_at is in ISO 8601 format (YYYY-MM-DDTHH:MM:SS)
- Return ONLY the SQL query, no explanations or markdown

User question: {question}

SQL query:"""

# Промпт для форматирования результатов
RESULTS_FORMAT_PROMPT = """Format the SQL query results into a clear, human-readable response in Russian.

User question: {question}
SQL query: {sql_query}
Query results: {results}

Provide a concise answer in Russian that directly answers the user's question."""


class TextToSQLService:
    """Сервис для обработки text-to-SQL запросов"""

    def __init__(self, config: Config, database: Database, logger: structlog.BoundLogger) -> None:
        """Инициализация сервиса text-to-SQL

        Args:
            config: Конфигурация приложения
            database: Менеджер подключений к базе данных
            logger: Логгер приложения
        """
        self.config = config
        self.database = database
        self.logger = logger
        self.llm_client = LLMClient(config, logger)

    def is_safe_query(self, sql: str) -> bool:
        """Проверка безопасности SQL запроса

        Разрешены только SELECT запросы без опасных операций.

        Args:
            sql: SQL запрос для проверки

        Returns:
            True если запрос безопасный, False иначе
        """
        # Нормализуем SQL: убираем лишние пробелы и переводим в верхний регистр
        normalized_sql = re.sub(r"\s+", " ", sql.strip().upper())

        # Запрещенные операции
        forbidden_keywords = [
            "DROP",
            "DELETE",
            "UPDATE",
            "INSERT",
            "ALTER",
            "CREATE",
            "TRUNCATE",
            "REPLACE",
            "PRAGMA",
            "ATTACH",
            "DETACH",
        ]

        # Проверка на запрещенные ключевые слова
        for keyword in forbidden_keywords:
            if keyword in normalized_sql:
                self.logger.warning("unsafe_sql_detected", sql=sql, forbidden_keyword=keyword)
                return False

        # Запрос должен начинаться с SELECT
        if not normalized_sql.startswith("SELECT"):
            self.logger.warning("non_select_query", sql=sql)
            return False

        return True

    async def generate_sql_from_question(self, question: str) -> str:
        """Генерация SQL запроса из вопроса пользователя

        Args:
            question: Вопрос пользователя на естественном языке

        Returns:
            SQL запрос

        Raises:
            ValueError: Если LLM не смог сгенерировать корректный SQL
        """
        # Формируем промпт для LLM
        prompt = TEXT_TO_SQL_PROMPT.format(question=question)

        # Генерируем SQL через LLM
        messages = [{"role": "user", "content": prompt}]
        sql_response = await self.llm_client.generate_response(messages)

        # Очистка ответа от markdown и лишних символов
        sql = sql_response.strip()
        sql = re.sub(r"```sql\n?", "", sql)
        sql = re.sub(r"```\n?", "", sql)
        sql = sql.strip()

        self.logger.info("sql_generated", question=question, sql=sql)

        # Проверка безопасности
        if not self.is_safe_query(sql):
            raise ValueError("Generated SQL query is not safe")

        return sql

    async def execute_sql_query(self, sql: str) -> list[dict]:
        """Выполнение SQL запроса

        Args:
            sql: SQL запрос для выполнения

        Returns:
            Результаты запроса в виде списка словарей

        Raises:
            Exception: При ошибках выполнения запроса
        """
        async with self.database.get_connection() as conn:
            # Устанавливаем timeout для запроса (5 секунд)
            await conn.execute("PRAGMA busy_timeout = 5000")

            cursor = await conn.execute(sql)
            rows = await cursor.fetchall()

            # Конвертация Row в dict
            results = [dict(row) for row in rows]

            self.logger.info("sql_executed", sql=sql, row_count=len(results))

            return results

    async def format_results(self, question: str, sql: str, results: list[dict]) -> str:
        """Форматирование результатов SQL в человекочитаемый ответ

        Args:
            question: Исходный вопрос пользователя
            sql: Выполненный SQL запрос
            results: Результаты запроса

        Returns:
            Отформатированный ответ на русском языке
        """
        # Ограничим количество результатов для промпта (максимум 20)
        limited_results = results[:20]
        results_str = str(limited_results)

        # Если результатов больше 20, добавим примечание
        if len(results) > 20:
            results_str += f"\n... (показано 20 из {len(results)} записей)"

        # Формируем промпт
        prompt = RESULTS_FORMAT_PROMPT.format(question=question, sql_query=sql, results=results_str)

        # Генерируем ответ через LLM
        messages = [{"role": "user", "content": prompt}]
        formatted_response = await self.llm_client.generate_response(messages)

        return formatted_response

    async def process_message(self, request: ChatRequest) -> ChatResponse:
        """Обработка сообщения в admin режиме (text-to-SQL)

        Pipeline:
        1. Вопрос пользователя → генерация SQL через LLM
        2. Выполнение SQL запроса к БД
        3. Форматирование результатов через LLM
        4. Возврат ответа с SQL запросом

        Args:
            request: Запрос от пользователя

        Returns:
            Ответ с сообщением и SQL запросом

        Raises:
            Exception: При ошибках на любом этапе pipeline
        """
        user_id = session_id_to_user_id(request.session_id)

        self.logger.info(
            "text_to_sql_request",
            session_id=request.session_id,
            user_id=user_id,
            question=request.message,
        )

        try:
            # 1. Генерация SQL запроса
            sql = await self.generate_sql_from_question(request.message)

            # 2. Выполнение SQL
            results = await self.execute_sql_query(sql)

            # 3. Форматирование результатов
            formatted_response = await self.format_results(request.message, sql, results)

            self.logger.info(
                "text_to_sql_response",
                session_id=request.session_id,
                user_id=user_id,
                sql=sql,
                result_count=len(results),
            )

            return ChatResponse(message=formatted_response, sql_query=sql, session_id=request.session_id)

        except ValueError as e:
            # Ошибка безопасности SQL
            error_message = f"❌ Не удалось выполнить запрос: {str(e)}"
            self.logger.warning("text_to_sql_validation_error", session_id=request.session_id, error=str(e))
            return ChatResponse(message=error_message, sql_query=None, session_id=request.session_id)

        except Exception as e:
            # Общая ошибка
            error_message = f"❌ Произошла ошибка при обработке запроса: {str(e)}"
            self.logger.error(
                "text_to_sql_error",
                session_id=request.session_id,
                user_id=user_id,
                error=str(e),
                exc_info=True,
            )
            return ChatResponse(message=error_message, sql_query=None, session_id=request.session_id)
