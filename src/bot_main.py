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

async def run_bot():
    """Главная функция запуска бота"""
    # Инициализация БД
    await init_db()
    logger.info("База данных инициализирована")
    
    # Подключение к VK API
    try:
        vk_session = vk_api.VkApi(token=settings.VK_TOKEN)
        vk = vk_session.get_api()
        
        # Проверка подключения
        group_info = vk.groups.getById(group_id=settings.VK_GROUP_ID)
        logger.info(f"Бот подключен к группе: {group_info[0]['name']}")
        
        # Long Poll для получения событий
        longpoll = VkBotLongPoll(vk_session, settings.VK_GROUP_ID)
        
        logger.info("🚀 Бот успешно запущен и ожидает сообщений...")
        
        for event in longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                user_id = event.obj.message['from_id']
                text = event.obj.message.get('text', '').strip()
                
                # Лимит запросов
                if not rate_limiter.check_rate_limit(user_id):
                    vk.messages.send(
                        user_id=user_id,
                        random_id=get_random_id(),
                        message="⏳ Вы слишком часто отправляете запросы. Подождите немного."
                    )
                    continue
                
                # Обработка команд
                if text.lower() in ['/start', 'начать']:
                    await handle_start_command(vk, user_id)
                elif text.lower() in ['/help', 'помощь']:
                    await handle_help_command(vk, user_id)
                elif text.lower().startswith('/report'):
                    await handle_report_command(vk, user_id, text)
                else:
                    vk.messages.send(
                        user_id=user_id,
                        random_id=get_random_id(),
                        message="❓ Команда не распознана. Используйте /help для списка команд."
                    )
    
    except Exception as e:
        logger.error(f"Критическая ошибка бота: {e}")
        raise
