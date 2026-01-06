import re

with open('src/bot_main.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Добавляем функцию handle_zouit_guide перед handle_report_command
zouit_function = '''async def handle_zouit_guide(vk: VkApi, user_id: int) -> None:
    """Обработка команды Справочник ЗОУИТ"""
    metrics.increment_command_counter('zouit_guide')
    
    step = get_dialog_step('zouit_guide')
    send_message(vk, user_id, step.text)

'''

# Находим позицию handle_report_command
pattern = r'(async def handle_report_command)'
if re.search(pattern, content):
    content = re.sub(pattern, zouit_function + r'\1', content)
    print('✅ Добавлена функция handle_zouit_guide')
else:
    print('❌ Не найдена handle_report_command')

# 2. Добавляем обработчик в раздел обработки сообщений
# Ищем elif text.lower().startswith('/report'): и добавляем перед ним
handler_code = '''                elif "справочник" in text.lower():
                    await handle_zouit_guide(vk, user_id)
                '''

pattern2 = r"(\s+elif text\.lower\(\)\.startswith\('/report'\):)"
if re.search(pattern2, content):
    content = re.sub(pattern2, handler_code + r'\1', content)
    print('✅ Добавлен обработчик elif "справочник"')
else:
    print('❌ Не найден elif text.lower().startswith')

with open('src/bot_main.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('\n✨ Файл bot_main.py успешно обновлён!')
