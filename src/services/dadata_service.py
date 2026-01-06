"""DaData API сервис для работы с адресами и организациями"""
import os
from typing import List, Dict, Optional
from dadata import Dadata
import logging

logger = logging.getLogger(__name__)

class DaDataService:
    """Сервис для работы с DaData API"""
    
    def __init__(self):
        self.api_key = os.getenv('DADATA_API_KEY')
        self.secret_key = os.getenv('DADATA_SECRET_KEY')
        
        if not self.api_key or not self.secret_key:
            raise ValueError("Не найдены API ключи DaData в .env файле")
        
        self.dadata = Dadata(self.api_key, self.secret_key)
        self.request_count = 0
        self.MAX_DAILY_REQUESTS = 10000
        logger.info("🌐 DaData сервис инициализирован")
    
    def check_rate_limit(self) -> bool:
        """Проверка лимита запросов"""
        if self.request_count >= self.MAX_DAILY_REQUESTS:
            logger.warning(f"⚠️ Достигнут дневной лимит {self.MAX_DAILY_REQUESTS} запросов")
            return False
        return True
    
    def increment_counter(self):
        """Увеличение счетчика запросов"""
        self.request_count += 1
    
    def suggest_address(self, query: str, count: int = 5) -> List[Dict]:
        """
        Получение подсказок по адресу
        
        Args:
            query: Частичный адрес для поиска
            count: Количество подсказок (max 20)
        
        Returns:
            Список подсказок с адресами
        """
        if not self.check_rate_limit():
            return []
        
        if len(query) < 3:
            logger.warning("⚠️ Запрос слишком короткий (мин. 3 символа)")
            return []
        
        try:
            result = self.dadata.suggest("address", query, count=count)
            self.increment_counter()
            logger.info(f"📍 Найдено {len(result)} подсказок для '{query}'")
            return result
        except Exception as e:
            logger.error(f"❌ Ошибка DaData API: {e}")
            return []
    
    def clean_address(self, address: str) -> Optional[Dict]:
        """
        Стандартизация и разбор адреса
        
        Args:
            address: Адрес для стандартизации
        
        Returns:
            Стандартизированный адрес
        """
        if not self.check_rate_limit():
            return None
        
        try:
            result = self.dadata.clean("address", address)
            self.increment_counter()
            logger.info(f"✅ Адрес стандартизирован: {address}")
            return result
        except Exception as e:
            logger.error(f"❌ Ошибка DaData API: {e}")
            return None
    
    def format_address_suggestions(self, suggestions: List[Dict]) -> str:
        """
        Форматирование подсказок для отправки пользователю
        
        Args:
            suggestions: Список подсказок
        
        Returns:
            Форматированный текст
        """
        if not suggestions:
            return "❌ Адрес не найден. Попробуйте уточнить запрос."
        
        result = "📍 Найдены адреса:\n\n"
        for i, suggestion in enumerate(suggestions[:5], 1):
            address = suggestion.get('value', 'Неизвестно')
            result += f"{i}. {address}\n"
        
        result += "\nВыберите номер нужного адреса."
        return result

