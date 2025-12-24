"""
Zemlya Bot VK - Main Bot Class
Основной класс бота
"""

import asyncio
import logging
from typing import Dict, List, Optional
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.utils import get_random_id

from .config import config
from .database import Database
from .data_sources import DataSourceManager
from .payment import PaymentManager
from .utils.rate_limiter import RateLimiter
from .utils.metrics import MetricsCollector


class ZemlyaBot:
    """
    Главный класс VK бота для анализа земельных участков
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # VK API
        self.vk_session = vk_api.VkApi(token=config.VK_TOKEN)
        self.vk = self.vk_session.get_api()
        self.longpoll = VkBotLongPoll(self.vk_session, config.VK_GROUP_ID)
        
        # Components
        self.db = Database()
        self.data_sources = DataSourceManager()
        self.payments = PaymentManager()
        self.rate_limiter = RateLimiter()
        self.metrics = MetricsCollector()
        
    def send_message(self, user_id: int, message: str):
        try:
            self.vk.messages.send(
                user_id=user_id,
                message=message,
                random_id=get_random_id()
            )
        except Exception as e:
            self.logger.error(f"Error: {e}")

    async def run(self):
        for event in self.longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                user_id = event.obj.message['from_id']
                text = event.obj.message['text']
                self.send_message(user_id, f"Echo: {text}")
