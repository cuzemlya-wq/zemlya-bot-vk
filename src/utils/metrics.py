"""Простой сборщик метрик."""

from collections import defaultdict
from typing import Dict, Any, Optional


class MetricsCollector:
    """
    Очень простой сборщик метрик в памяти.
    Пока просто считает количество событий по имени.
    """

    def __init__(self) -> None:
        # name -> count
        self._counters: Dict[str, int] = defaultdict(int)

    def increment(self, name: str, tags: Optional[Dict[str, Any]] = None) -> None:
        """
        Увеличивает счётчик метрики с указанным именем.
        tags сейчас игнорируются, но параметр оставлен на будущее.
        
        Args:
            name: Имя метрики
            tags: Дополнительные теги (пока не используются)
        """
        self._counters[name] += 1

    def get_counters(self) -> Dict[str, int]:
        """
        Возвращает текущие значения всех счётчиков.
        
        Returns:
            Словарь с метриками
        """
        return dict(self._counters)


# Глобальный экземпляр
metrics = MetricsCollector()
