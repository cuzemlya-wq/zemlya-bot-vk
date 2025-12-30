import time
from collections import defaultdict
from typing import Dict

class RateLimiter:
    def __init__(self, max_requests: int = 5, time_window: int = 60):
        """
        Ограничение частоты запросов
        :param max_requests: Макс. кол-во запросов за время
        :param time_window: Временное окно в секундах
        """
        self.max_requests = max_requests
        self.time_window = time_window
        self.requests: Dict[int, list] = defaultdict(list)
    
    def check_rate_limit(self, user_id: int) -> bool:
        """Проверка лимита для пользователя"""
        current_time = time.time()
        
        # Удаление старых запросов вне временного окна
        self.requests[user_id] = [
            req_time for req_time in self.requests[user_id]
            if current_time - req_time < self.time_window
        ]
        
        # Проверка лимита
        if len(self.requests[user_id]) >= self.max_requests:
            return False
        
        # Добавление нового запроса
        self.requests[user_id].append(current_time)
        return True

rate_limiter = RateLimiter(max_requests=10, time_window=60)
