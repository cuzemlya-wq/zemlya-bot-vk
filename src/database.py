"""Заглушка для работы с базой данных.

В будущем здесь будет реализована работа с:
- SQLAlchemy моделями
- Подключением к PostgreSQL
- Миграциями Alembic
"""

from src.utils.logger import get_logger

logger = get_logger(__name__)


class Database:
    """Класс для работы с базой данных."""
    
    def __init__(self):
        logger.info("Инициализация Database (заглушка)")
    
    async def connect(self):
        """Подключение к БД."""
        logger.info("Подключение к БД (заглушка)")
    
    async def disconnect(self):
        """Отключение от БД."""
        logger.info("Отключение от БД (заглушка)")
    
    async def save_user(self, user_id: int, username: str = None):
        """Сохранение пользователя."""
        logger.info(f"Сохранение пользователя {user_id} (заглушка)")
    
    async def save_report(self, user_id: int, cadastral_number: str, report_data: dict):
        """Сохранение отчёта."""
        logger.info(f"Сохранение отчёта для {cadastral_number} (заглушка)")
