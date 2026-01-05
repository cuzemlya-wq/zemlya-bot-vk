import re

with open('src/bot_main.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Находим цикл for event
pattern = r'(logger\.info\(".*?Бот успешно запущен.*?"\)\s+)(for event in longpoll\.listen\(\):)'

replacement = r'\1\n    # Дедупликация событий\n    processed_messages = set()\n    \n    \2'

content = re.sub(pattern, replacement, content, flags=re.DOTALL)

# Находим место после payload = event.obj.message.get('payload')
pattern2 = r"(payload = event\.obj\.message\.get\('payload'\))(\s+)(# Лимит запросов)"

replacement2 = r"\1\n            message_id = event.obj.message.get('id')\n            \n            # Проверка на дубликаты\n            if message_id in processed_messages:\n                continue\n            processed_messages.add(message_id)\n            \n            # Ограничение размера set (10000 последних сообщений)\n            if len(processed_messages) > 10000:\n                processed_messages.clear()\n\2\3"

content = re.sub(pattern2, replacement2, content)

with open('src/bot_main.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('Файл успешно исправлен!')
