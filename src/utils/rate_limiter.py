"""Простой in-memory rate limiter."""

import time
from collections import defaultdict
from typing import Dict, List

from src.config import settings


class RateLimiter:
    """
    Простейший in-memory rate limiter.
    Ограничивает количество запросов за период для одного ключа.
    """

    def __init__(self, limit: int = None, period: int = None) -> None:
        """
        Args:
            limit: сколько запросов можно сделать
            period: за какой период (секунд)
        """
        self.limit = limit or settings.rate_limit_requests
        self.period = period or settings.rate_limit_period
        self._storage: Dict[str, List[float]] = defaultdict(list)

    async def is_allowed(self, key: str) -> bool:
        """
        Возвращает True, если запрос можно выполнить.
        
        Args:
            key: Ключ для лимитирования (например, "user:12345")
        
        Returns:
            True если можно, False если лимит превышен
        """
        now = time.time()
        window_start = now - self.period

        timestamps = self._storage[key]

        # Оставляем только те вызовы, которые были в пределах окна
        timestamps = [t for t in timestamps if t > window_start]
        self._storage[key] = timestamps

        if len(timestamps) >= self.limit:
            return False

        timestamps.append(now)
        return True


# Глобальный экземпляр
rate_limiter = RateLimiter()
