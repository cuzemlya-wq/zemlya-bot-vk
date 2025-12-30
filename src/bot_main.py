"""Основная логика VK бота."""

import asyncio
from vk_api import VkApi
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.utils import get_random_id

from src.config import settings
from src.utils.logger import get_logger

# Инициализируем логгер
logger = get_logger(__name__)


def send_message(vk: VkApi, peer_id: int, text: str) -> None:
    """
    Отправляет сообщение в VK.
    
    Args:
        vk: Экземпляр VkApi
        peer_id: ID получателя
        text: Текст сообщения
    """
    try:
        vk.messages.send(
            peer_id=peer_id,
            message=text,
            random_id=get_random_id()
        )
        logger.info(f"Отправлено сообщение для peer_id={peer_id}")
    except Exception as e:
        logger.error(f"Ошибка при отправке сообщения: {e}")


async def run_bot() -> None:
    """
    Запускает VK бота и слушает события.
    """
    logger.info("Запуск ЗемляVot v1.0...")
    logger.info(f"Окружение: {settings.environment}")
    logger.info(f"VK Group ID: {settings.vk_group_id}")
    
    try:
        # Инициализация VK API
        vk_session = VkApi(token=settings.vk_token)
        vk = vk_session.get_api()
        
        # Инициализация Long Poll
        longpoll = VkBotLongPoll(vk_session, settings.vk_group_id)
        
        logger.info("Бот успешно запущен и готов к обработке сообщений!")
        
        # Основной цикл обработки событий
        for event in longpoll.listen():
            # Обрабатываем только новые сообщения
            if event.type == VkBotEventType.MESSAGE_NEW:
                peer_id = event.obj.message['peer_id']
                text = event.obj.message['text'].strip()
                
                logger.info(f"Получено сообщение от {peer_id}: {text}")
                
                # Обрабатываем команды
                if text.lower() == '/start':
                    response = (
                        "Привет! 👋\n\n"
                        "Я - ЗемляVot, бот для анализа земельных участков.\n\n"
                        "Чтобы узнать, что я умею, напишите /help"
                    )
                    send_message(vk, peer_id, response)
                    
                elif text.lower() == '/help':
                    response = (
                        "🔍 Доступные команды:\n\n"
                        "/start - Начать работу с ботом\n"
                        "/help - Показать это сообщение\n\n"
                        "🚀 Скоро будет доступен полный анализ участков!"
                    )
                    send_message(vk, peer_id, response)
                    
                else:
                    response = (
                        "Я пока понимаю только команды:\n"
                        "/start - Начать работу\n"
                        "/help - Помощь"
                    )
                    send_message(vk, peer_id, response)
    
    except KeyboardInterrupt:
        logger.info("Бот остановлен пользователем")
    except Exception as e:
        logger.error(f"Критическая ошибка: {e}", exc_info=True)
        raise
