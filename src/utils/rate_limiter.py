"""Заглушка для rate limiter (ограничение частоты запросов).

В будущем:
- Ограничение запросов на пользователя
- Использование Redis для хранения счётчиков
"""

from src.utils.logger import get_logger

logger = get_logger(__name__)


class RateLimiter:
    """Класс для ограничения частоты запросов."""
    
    def __init__(self):
        logger.info("Инициализация RateLimiter (заглушка)")
    
    async def check_limit(self, user_id: int) -> bool:
        """
        Проверяет, может ли пользователь сделать запрос.
        
        Args:
            user_id: ID пользователя
        
        Returns:
            True, если можно, False иначе
        """
        # Заглушка - всегда разрешаем
        return True
