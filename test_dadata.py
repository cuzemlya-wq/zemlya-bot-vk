"""Test DaData integration"""
import os
from dotenv import load_dotenv
from src.services.dadata_service import DaDataService

load_dotenv()

def test_address_suggest():
    print("📦 Тестирование DaData API")
    print("-" * 50)
    
    # Инициализация сервиса
    service = DaDataService()
    
    # Тестовые запросы
    test_queries = [
        "Москва Ленина 10",
        "Санкт-Петербург Невский",
        "Новосибирск Красный"
    ]
    
    for query in test_queries:
        print(f"\n🔍 Запрос: {query}")
        suggestions = service.suggest_address(query, count=3)
        
        if suggestions:
            for i, suggestion in enumerate(suggestions, 1):
                address = suggestion.get('value', 'Неизвестно')
                print(f"  {i}. {address}")
        else:
            print("  ❌ Ничего не найдено")
    
    print(f"\n📊 Использовано запросов: {service.request_count}")
    print("✅ Тест завершен")

if __name__ == "__main__":
    test_address_suggest()
