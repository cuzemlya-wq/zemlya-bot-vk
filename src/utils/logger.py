"""Модуль для настройки логирования."""

import logging
import sys
from typing import Optional

from src.config import settings


def get_logger(name: str, level: Optional[str] = None) -> logging.Logger:
    """
    Создаёт и настраивает логгер.
    
    Args:
        name: Имя логгера
        level: Уровень логирования (по умолчанию из settings)
    
    Returns:
        Настроенный логгер
    """
    logger = logging.getLogger(name)
    
    # Устанавливаем уровень логирования
    log_level = level or settings.log_level
    logger.setLevel(getattr(logging, log_level.upper()))
    
    # Если уже есть обработчики, не добавляем новые
    if logger.handlers:
        return logger
    
    # Создаём обработчик для вывода в консоль
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(getattr(logging, log_level.upper()))
    
    # Формат логов
    formatter = logging.Formatter(
        fmt='[%(levelname)s] %(name)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler.setFormatter(formatter)
    
    logger.addHandler(console_handler)
    
    return logger
