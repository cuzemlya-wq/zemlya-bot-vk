with open('src/bot_main.py', 'r') as f:
    lines = f.readlines()

# Найти строку 218 (elif text_lower in ['/help'...])
for i, line in enumerate(lines):
    if "elif text_lower in ['/help'" in line:
        # Вставить после неё handle_help_command
        # Потом найти следующий elif
        j = i + 1
        while j < len(lines) and not lines[j].strip().startswith('elif'):
            j += 1
        # Вставить zouit_guide перед следующим elif
        zouit_code = """                elif 'справочник' in text_lower or 'зоуит' in text_lower:
                    await handle_zouit_guide(vk, user_id)
"""
        lines.insert(j, zouit_code)
        break

with open('src/bot_main.py', 'w') as f:
    f.writelines(lines)

print('✅ ZOUIT guide добавлен')
