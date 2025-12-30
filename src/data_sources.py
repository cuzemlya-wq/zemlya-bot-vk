"""Источники данных о земельных участках.

Пока возвращаются фейковые данные для разработки.
В будущем здесь будет интеграция с реальными API.
"""

from typing import Dict, Any
from src.utils.logger import get_logger

logger = get_logger(__name__)


async def get_full_report(cadastral_number: str) -> Dict[str, Any]:
    """
    Возвращает фейковые данные по участку.
    Потом здесь можно будет сделать реальные запросы к API.
    
    Args:
        cadastral_number: Кадастровый номер
    
    Returns:
        Данные об участке
    """
    # TODO: заменить на реальные запросы к Росреестру, ПКК, рынку и т.д.
    logger.info(f"Получение данных по кадастровому номеру {cadastral_number}")
    
    return {
        "cadastral_number": cadastral_number,
        "area": 1200,  # кв. м
        "estimated_price": 3_500_000,  # руб
        "risk_level": "низкий",
        "notes": "Фейковые данные для разработки. Реальные API ещё не подключены."
    }
