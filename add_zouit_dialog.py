import re

with open('src/dialog_flows.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Найти последнюю запись перед закрывающей скобкой DIALOG_FLOWS
zouit_entry = '''    ,
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
    )'''

# Вставить перед закрывающей скобкой DIALOG_FLOWS (строка с одиночной })
pattern = r'(\n)(}\n\n# Функция для получения шага диалога)'
replacement = r'\g<1>' + zouit_entry + r'\n\g<2>'

content_new = re.sub(pattern, replacement, content)

if content_new != content:
    with open('src/dialog_flows.py', 'w', encoding='utf-8') as f:
        f.write(content_new)
    print("✅ Добавлен zouit_guide в DIALOG_FLOWS")
else:
    print("❌ Не удалось найти место для вставки")
