import asyncio
import random

async def get_fake_land_data(cadastral_number: str) -> dict:
    """Фейковые данные для тестирования"""
    await asyncio.sleep(1.5)
    
    return {
        'cadastral_number': cadastral_number,
        'address': f'г. Москва, ул. Примерная, д. {random.randint(1, 100)}',
        'area_sqm': random.randint(500, 5000),
        'category': random.choice(['Земли населённых пунктов', 'Земли сельскохозяйственного назначения', 'Земли промышленности']),
        'market_price': random.randint(5000000, 25000000),
        'cadastral_price': random.randint(3000000, 15000000),
        'risks': random.choice(['Не выявлено', 'Низкий уровень риска', 'Возможны ограничения']),
        'recommendations': random.choice(['Рекомендуется к покупке', 'Требуется дополнительная проверка', 'Хорошее предложение'])
    }
