"""Диалоговые потоки для многоступенчатой воронки продаж"""

from typing import Dict, List, Optional
from dataclasses import dataclass

@dataclass
class DialogStep:
    """Шаг диалога"""
    text: str
    buttons: List[Dict[str, str]]
    next_flow: Optional[str] = None

# Структура диалоговых потоков
DIALOG_FLOWS = {
    "greeting": DialogStep(
        text="""👋 Здравствуйте! Я ЗемляВот — помогаю с анализом земельных участков.

Я могу:
• Проверить юридическую чистоту участка
• Оценить рыночную стоимость
• Выявить скрытые риски и обременения
• Дать рекомендации по использованию

Что вас интересует?""",
        buttons=[
            {"label": "🔍 Проверить участок", "payload": "check_plot"},
            {"label": "💰 Узнать стоимость", "payload": "pricing"},
            {"label": "❓ Как это работает", "payload": "how_it_works"}
        ]
    ),
    
    "qualification_buyer": DialogStep(
        text="""Отлично! Чтобы дать максимально точный анализ, уточните:

Вы планируете покупку участка или уже являетесь собственником?""",
        buttons=[
            {"label": "🏡 Планирую купить", "payload": "buyer"},
            {"label": "✅ Уже собственник", "payload": "owner"},
            {"label": "🤔 Просто изучаю рынок", "payload": "researcher"}
        ]
    ),
    
    "buyer_urgency": DialogStep(
        text="""Понял! Покупка земли — серьёзный шаг.

На какой стадии находится ваша сделка?""",
        buttons=[
            {"label": "⚡ Уже нашёл участок", "payload": "urgent"},
            {"label": "🔎 Активно ищу", "payload": "active"},
            {"label": "📋 Присматриваюсь", "payload": "browsing"}
        ]
    ),
    
    "urgent_buyer": DialogStep(
        text="""⚠️ ВАЖНО! Перед покупкой обязательно проверьте:

1️⃣ Обременения и аресты
2️⃣ Соответствие документов реальным границам
3️⃣ Скрытые долги и налоги
4️⃣ Возможность подключения коммуникаций

90% проблем выявляются на этапе проверки!

Хотите получить БЕСПЛАТНУЮ экспресс-проверку вашего участка?""",
        buttons=[
            {"label": "✅ Да, проверить!", "payload": "request_report"},
            {"label": "📞 Сначала проконсультироваться", "payload": "consultation"},
            {"label": "⬅️ Назад", "payload": "back"}
        ]
    ),
    
    "pricing": DialogStep(
        text="""💎 Наши услуги:

🔍 ЭКСПРЕСС-ПРОВЕРКА (БЕСПЛАТНО)
• Проверка по базе Росреестра
• Выявление обременений
• Результат за 10 минут

📊 БАЗОВЫЙ ОТЧЁТ — 2.8-3.2 тыс. ₽
• Полная юридическая проверка
• Рыночная оценка
• Анализ рисков
• Готовность 1-2 часа

🏆 РАСШИРЕННЫЙ АНАЛИЗ — 5-10 тыс. ₽
• Всё из Базового
• Проверка коммуникаций
• Градостроительный план
• Рекомендации по использованию
• Личная консультация эксперта

Что вас интересует?""",
        buttons=[
            {"label": "🆓 Бесплатная проверка", "payload": "free_check"},
            {"label": "📊 Базовый отчёт", "payload": "basic_report"},
            {"label": "🏆 Расширенный", "payload": "premium_report"},
            {"label": "⬅️ Назад", "payload": "greeting"}
        ]
    ),
    
    "how_it_works": DialogStep(
        text="""🔧 Как работает проверка:

1️⃣ Вы даёте кадастровый номер участка
2️⃣ Мы запрашиваем данные из Росреестра
3️⃣ Система анализирует 10+ источников
4️⃣ Вы получаете понятный отчёт

⏱ Экспресс-проверка — 10 мин
📄 Полный отчёт — 1-2 часа

Всё онлайн, без визитов в офис!

Попробуем?""",
        buttons=[
            {"label": "✅ Да, попробовать!", "payload": "request_report"},
            {"label": "💰 Сколько стоит?", "payload": "pricing"},
            {"label": "⬅️ Назад", "payload": "greeting"}
        ]
    ),
    
    "request_report": DialogStep(
        text="""📋 Отлично! Для проверки мне нужен кадастровый номер участка.

Формат: XX:XX:XXXXXXX:XXX
Пример: 77:01:0001001:123

Отправьте команду:
/report ВАШ_КАДАСТРОВЫЙ_НОМЕР

Или нажмите кнопку для примера:""",
        buttons=[
            {"label": "📝 Пример: /report 77:01:0001001:123", "payload": "example_report"},
            {"label": "❓ Где найти номер?", "payload": "find_cadastral"},
            {"label": "⬅️ Назад", "payload": "greeting"}
        ]
    ),
    
    "find_cadastral": DialogStep(
        text="""🔍 Где найти кадастровый номер:

1️⃣ В документах на участок (свидетельство, договор)
2️⃣ На сайте Росреестра (rosreestr.gov.ru)
3️⃣ В выписке ЕГРН
4️⃣ На публичной кадастровой карте

Формат: XX:XX:XXXXXXX:XXX

Когда найдёте — отправьте:
/report ВАШ_НОМЕР""",
        buttons=[
            {"label": "📝 Пример проверки", "payload": "example_report"},
            {"label": "⬅️ Назад", "payload": "request_report"}
        ]
    ),
    
    "consultation": DialogStep(
        text="""📞 Консультация эксперта:

Наши специалисты работают 24/7 и готовы ответить на любые вопросы:

• Выбор участка
• Юридические риски
• Оценка стоимости
• Порядок сделки
• Подводные камни

💬 Напишите ваш вопрос прямо здесь, и эксперт ответит в течение 5-10 минут!

Или закажите обратный звонок:""",
        buttons=[
            {"label": "📞 Заказать звонок", "payload": "callback"},
            {"label": "📊 Сделать проверку", "payload": "request_report"},
            {"label": "⬅️ Назад", "payload": "greeting"}
        ]
    ),
    
    "callback": DialogStep(
        text="""📱 Обратный звонок:

Оставьте ваш номер телефона, и мы перезвоним в течение 15 минут!

Формат: +7 (XXX) XXX-XX-XX

Или напишите удобное время для звонка.""",
        buttons=[
            {"label": "⬅️ Назад", "payload": "consultation"}
        ]
    )
}
 ,
    "zouit_guide": DialogStep(
        text="""📋 Справочник ЗОУИТ

🔍 Здесь вы можете узнать о зонах с особыми условиями использования территорий:

• Что такое ЗОУИТ
• Виды ограничений
• Как проверить участок
• Куда обратиться за консультацией

Используйте кнопки ниже для навигации.""",
        buttons=[
            {"label": "🏠 Главное меню", "payload": "greeting"},
            {"label": "📞 Связаться", "payload": "contact"}
        ]
    )

def get_dialog_step(flow_name: str) -> Optional[DialogStep]:
    """Получить шаг диалога по имени"""
    return DIALOG_FLOWS.get(flow_name)

def format_buttons_for_vk(buttons: List[Dict[str, str]]) -> str:
    """Форматировать кнопки для VK API (JSON для клавиатуры)"""
    import json
    
    keyboard = {
        "one_time": False,
        "buttons": []
    }
    
    for button in buttons:
        keyboard["buttons"].append([
            {
                "action": {
                    "type": "text",
                    "label": button["label"],
                    "payload": json.dumps({"button": button["payload"]})
                },
                "color": "primary" if "Да" in button["label"] or "проверить" in button["label"].lower() else "secondary"
            }
        ])
    
    return json.dumps(keyboard, ensure_ascii=False)
