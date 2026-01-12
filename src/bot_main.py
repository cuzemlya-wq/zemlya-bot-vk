import re
import json
import asyncio
from vk_api import VkApi
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.utils import get_random_id

from src.config import settings
from src.utils.logger import get_logger
from src.database import init_db, save_user, save_report, get_user_flow
from src.data_sources import get_fake_land_data
from src.rate_limiter import rate_limiter
from src.metrics import metrics
from src.dialog_flows import get_dialog_step, format_buttons_for_vk

logger = get_logger(__name__)

def send_message(vk: VkApi, user_id: int, text: str, keyboard: str = None) -> None:
    """Отправка сообщения с клавиатурой"""
    try:
        params = {
            "user_id": user_id,
            "message": text,
            "random_id": get_random_id()
        }
        
        if keyboard:
            params["keyboard"] = keyboard
        
        vk.messages.send(**params)
        logger.info(f"Отправлено сообщение для user_id={user_id}")
    except Exception as e:
        logger.error(f"Ошибка отправки сообщения: {e}")

async def handle_dialog_flow(vk: VkApi, user_id: int, flow_name: str) -> None:
    """Обработка диалогового потока"""
    dialog_step = get_dialog_step(flow_name)
    
    if not dialog_step:
        logger.warning(f"Неизвестный диалог: {flow_name}")
        flow_name = "greeting"
        dialog_step = get_dialog_step(flow_name)
    
    # Сохраняем текущее состояние
    await save_user(user_id, flow_name)
    
    # Формируем клавиатуру
    keyboard = format_buttons_for_vk(dialog_step.buttons)
    
    # Отправляем сообщение
    send_message(vk, user_id, dialog_step.text, keyboard)
    
    # Увеличиваем метрику
    metrics.increment_command_counter(f"flow:{flow_name}")

async def handle_button_click(vk: VkApi, user_id: int, payload: str) -> None:
    """Обработка нажатия кнопки"""
    try:
        payload_data = json.loads(payload)
        button_action = payload_data.get("button")
        
        if not button_action:
            return
        
        logger.info(f"User {user_id} clicked button: {button_action}")
        
        # Особые случаи
        if button_action == "example_report":
            await handle_report_command(vk, user_id, "/report 77:01:0001001:123")
            return
        elif button_action == "back":
            # Возвращаемся к предыдущему шагу
            button_action = "greeting"
        elif button_action in ["check_plot", "free_check"]:
            button_action = "qualification_buyer"
        elif button_action == "buyer":
            button_action = "buyer_urgency"
        elif button_action == "urgent":
            button_action = "urgent_buyer"
        elif button_action in ["basic_report", "premium_report"]:
            button_action = "request_report"
        
        # Переходим к новому диалогу
        await handle_dialog_flow(vk, user_id, button_action)
        
    except json.JSONDecodeError:
        logger.error(f"Invalid payload: {payload}")
    except Exception as e:
        logger.error(f"Ошибка обработки кнопки: {e}")

async def handle_start_command(vk: VkApi, user_id: int) -> None:
    """Обработка команды /start"""
    metrics.increment_command_counter('/start')
    await handle_dialog_flow(vk, user_id, "greeting")

async def handle_help_command(vk: VkApi, user_id: int) -> None:
    """Обработка команды /help"""
    metrics.increment_command_counter('/help')
    
    help_text = """📚 Доступные команды:

/start — Начать работу с ботом
/help — Помощь
/report <кадастровый номер> — Получить отчет

📋 Пример:
/report 77:01:0001001:123

Или используйте кнопки для навигации! 👇"""
    
    send_message(vk, user_id, help_text)

async def handle_zouit_guide(vk: VkApi, user_id: int) -> None:
    metrics.increment_command_counter('zouit_guide')
    
    step = get_dialog_step('zouit_guide')
    send_message(vk, user_id, step.text)

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
✅ Рекомендации: {land_data['recommendations']}

---
📞 Хотите получить расширенный анализ? Нажмите кнопку ниже!"""
        
        # Клавиатура с предложением услуги
        keyboard = format_buttons_for_vk([
            {"label": "🏆 Расширенный отчёт", "payload": "pricing"},
            {"label": "📞 Консультация", "payload": "consultation"},
            {"label": "🏠 Главное меню", "payload": "greeting"}
        ])
        
        send_message(vk, user_id, report, keyboard)
        metrics.increment_reports_generated()
        
    except Exception as e:
        logger.error(f"Ошибка при получении данных: {e}")
        send_message(vk, user_id, "❌ Ошибка при получении данных. Попробуйте позже.")

async def run_bot():
    """Главная функция запуска бота с диалогами"""
    await init_db()
    logger.info("База данных инициализирована")
    
    try:
        vk_session = VkApi(token=settings.VK_TOKEN)
        vk = vk_session.get_api()
        
        group_info = vk.groups.getById(group_id=settings.VK_GROUP_ID)
        logger.info(f"Бот подключен к группе: {group_info[0]['name']}")
        
        longpoll = VkBotLongPoll(vk_session, settings.VK_GROUP_ID)
        
        logger.info("🚀 Бот успешно запущен с диалоговыми потоками и ожидает сообщений...")
        
        for event in longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                user_id = event.obj.message['from_id']
                text = event.obj.message.get('text', '').strip()
                payload = event.obj.message.get('payload')
                
                # Лимит запросов
                if not rate_limiter.check_rate_limit(user_id):
                    send_message(vk, user_id, "⏳ Вы слишком часто отправляете запросы. Подождите немного.")
                    continue
                
                # Обработка нажатия кнопки
                if payload:
                    await handle_button_click(vk, user_id, payload)
                    continue
                
                # Обработка текстовых команд
                text_lower = text.lower()
                
                if text_lower in ['/start', 'начать', 'привет', 'start']:
                    await handle_start_command(vk, user_id)
                elif text_lower in ['/help', 'помощь', 'help']:
                    await handle_help_command(vk, user_id)
                elif 'справочник' in text_lower or 'зоуит' in text_lower:
                    await handle_zouit_guide(vk, user_id)
                    await handle_zouit_guide(vk, user_id)
                await handle_zouit_guide(vk, user_id)
                elif text_lower.startswith('/report') or text_lower.startswith('отчет') or re.search(r'\d{2}:\d{2}:\d{7}:\d+', text):
                
                    await handle_report_command(vk, user_id, text)
                else:
                    # Ответ на нераспознанные сообщения
                    response_text = "❓ Команда не распознана. Используйте кнопки ниже или /help для списка команд."
                    
                    # Показываем главное меню
                    await handle_dialog_flow(vk, user_id, "greeting")
    
    except Exception as e:
        logger.error(f"Критическая ошибка бота: {e}")
        raise
