"""Заглушка для сбора метрик.

В будущем:
- Сбор метрик использования
- Аналитика запросов
- Мониторинг производительности
"""

from src.utils.logger import get_logger

logger = get_logger(__name__)


class MetricsCollector:
    """Класс для сбора метрик."""
    
    def __init__(self):
        logger.info("Инициализация MetricsCollector (заглушка)")
    
    async def track_request(self, user_id: int, request_type: str):
        """
        Отслеживает запрос.
        
        Args:
            user_id: ID пользователя
            request_type: Тип запроса
        """
        logger.debug(f"Отслеживание запроса {request_type} от {user_id} (заглушка)")
    
    async def get_stats(self) -> dict:
        """
        Получает статистику.
        
        Returns:
            Словарь со статистикой
        """
        logger.info("Получение статистики (заглушка)")
        return {"status": "stub"}
