#!/usr/bin/env python3
"""
Zemlya Bot VK - Entry Point
ВК бот для анализа земельных участков
"""

import asyncio
import logging
import sys
from pathlib import Path

# Добавляем корневую директорию в путь
sys.path.insert(0, str(Path(__file__).parent))

from src.bot_main import ZemlyaBot
from src.config import config
from src.utils.logger import setup_logger


def main():
    """
    Главная функция запуска бота
    """
    # Настройка логирования
    logger = setup_logger(
        name="zemlya_bot",
        log_level=config.LOG_LEVEL,
        log_file=config.LOG_FILE
    )
    
    logger.info("="*50)
    logger.info("Запуск Zemlya Bot VK")
    logger.info(f"Версия: 1.0.0")
    logger.info(f"Режим: {'Production' if config.PRODUCTION else 'Development'}")
    logger.info("="*50)
    
    try:
        # Создаем экземпляр бота
        bot = ZemlyaBot()
        
        # Запускаем бота
        logger.info("Бот инициализирован, начинаем работу...")
        asyncio.run(bot.run())
        
    except KeyboardInterrupt:
        logger.info("Получен сигнал остановки (Ctrl+C)")
        logger.info("Завершение работы бота...")
    except Exception as e:
        logger.critical(f"Критическая ошибка при запуске бота: {e}", exc_info=True)
        sys.exit(1)
    finally:
        logger.info("Бот остановлен")
        logger.info("="*50)


if __name__ == "__main__":
    main()
