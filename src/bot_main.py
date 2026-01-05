import re
import asyncio
from vk_api import VkApi
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.utils import get_random_id

from src.config import settings
from src.utils.logger import get_logger
from src.database import init_db, save_user, save_report
from src.data_sources import get_fake_land_data
from src.rate_limiter import rate_limiter
from src.metrics import metrics

logger = get_logger(__name__)

def send_message(vk: VkApi, peer_id: int, text: str) -> None:
    """Отправка сообщения"""
    try:
        vk.messages.send(
            peer_id=peer_id,
            message=text,
            random_id=get_random_id()
        )
        logger.info(f"Отправлено сообщение для peer_id={peer_id}")
    except Exception as e:
        logger.error(f"Ошибка отправки сообщения: {e}")

async def handle_start_command(vk: VkApi, user_id: int) -> None:
    """Обработка команды /start"""
    await save_user(user_id)
    metrics.increment_command_counter('/start')
    
    welcome_text = """🌍 Привет! Я ЗемляVot — бот для анализа земельных участков.

📝 Что я умею:
• Получать информацию по кадастровому номеру
• Анализировать рыночную стоимость
• Давать рекомендации по использованию

🕹 Напишите /help для списка команд."""
    
    send_message(vk, user_id, welcome_text)


sync def handle_zouit_guide(vk: VkApi, user_id: int) -> None:
    """Обработка команды 'Справочник ЗОУИТ'"""    metrics.increment_command_counter('/help')
    metrics.increment_command_counter('zouit_guide')

        step = get_dialog_step('zouit_guide')
            send_message(vk, user_id, step.text)

async def handle_report_command(vk: VkApi, user_id: int, text: str) -> None:
 

async def handle_help_command(vk: VkApi, user_id: int) -> None:
    """Обработка команды /help"""
    metrics.increment_command_counter('/help')
    
    help_text = """📚 Доступные команды:

/start — Начать работу с ботом
/help — Помощь
/report <кадастровый номер> — Получить отчет

📋 Пример:
/report 77:01:0001001:123"""
    
    send_message(vk, user_id, help_text)


async def handle_report_command(vk: VkApi, user_id: int, text: str) -> None:
    """Обработка команды /report"""
    metrics.increment_command_counter('/report')
    
    # Извлечение кадастрового номера
    match = re.search(r'\d{2}:\d{2}:\d{7}:\d+', text)
    if not match:
        send_message(vk, user_id, "❌ Неверный формат кадастрового номера.\n\n📝 Пример: /report 77:01:0001001:123")
        return
    
    cadastral_number = match.group()
    logger.info(f"Получен запрос на кадастр {cadastral_number} от user_id={user_id}")
    
    # Получение данных
    send_message(vk, user_id, "⏳ Запрашиваю данные... Подождите немного.")
    
    try:
        land_data = await get_fake_land_data(cadastral_number)
        
        # Сохранение в БД
        await save_report(user_id, cadastral_number, land_data)
        
        # Формирование отчета
        report = f"""📊 Отчет по участку: {land_data['cadastral_number']}

📍 Адрес: {land_data['address']}
📏 Площадь: {land_data['area_sqm']} м²
💼 Категория: {land_data['category']}

💰 Цены:
  • Рыночная: {land_data['market_price']:,.0f} ₽
  • Кадастровая: {land_data['cadastral_price']:,.0f} ₽

⚠️ Риски: {land_data['risks']}
✅ Рекомендации: {land_data['recommendations']}"""
        
        send_message(vk, user_id, report)
        metrics.increment_reports_generated()
        
    except Exception as e:
        logger.error(f"Ошибка при получении данных: {e}")
        send_message(vk, user_id, "❌ Ошибка при получении данных. Попробуйте позже.")

async def run_bot():
    """Главная функция запуска бота"""
    await init_db()
    logger.info("База данных инициализирована")
    
    try:
        vk_session = VkApi(token=settings.VK_TOKEN)
        vk = vk_session.get_api()
        
        group_info = vk.groups.getById(group_id=settings.VK_GROUP_ID)
        logger.info(f"Бот подключен к группе: {group_info[0]['name']}")
        
        longpoll = VkBotLongPoll(vk_session, settings.VK_GROUP_ID)
        
        logger.info("🚀 Бот успешно запущен и ожидает сообщений...")
        
        for event in longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                user_id = event.obj.message['from_id']
                text = event.obj.message.get('text', '').strip()
                
                if not rate_limiter.check_rate_limit(user_id):
                    vk.messages.send(
                        user_id=user_id,
                        random_id=get_random_id(),
                        message="⏳ Вы слишком часто отправляете запросы. Подождите немного."
                    )
                    continue
                
                if text.lower() in ['/start', 'начать']:
                    await handle_start_command(vk, user_id)
                elif text.lower() in ['/help', 'помощь']:
                    await handle_help_command(vk, user_id)
                elif text.lower().startswith('/report'):
                    await handle_report_command(vk, user_id, text)
                                elif "справочник" in text.lower():
                    await handle_zouit_guide(vk, user_id)                else:
                    vk.messages.send(
                        user_id=user_id,
                        random_id=get_random_id(),
                        message="❓ Команда не распознана. Используйте /help для списка команд."
                    )
    
    except Exception as e:
        logger.error(f"Критическая ошибка бота: {e}")
        raise
