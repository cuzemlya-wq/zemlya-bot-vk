import sys
sys.path.insert(0, 'src')

from dialog_flows import get_dialog_step

# Тест 1: Проверка загрузки zouit_guide
print("📝 Тест 1: Проверка dialog_flows")
zouit_step = get_dialog_step('zouit_guide')
if zouit_step:
    print("  ✅ zouit_guide найден!")
    print(f"  Текст: {zouit_step.text[:50]}...")
    print(f"  Кнопки: {len(zouit_step.buttons)} шт.")
else:
    print("  ❌ zouit_guide не найден")

# Тест 2: Проверка распознавания команд
print("\n📝 Тест 2: Распознавание команд")

test_texts = [
    "Справочник ЗОУИТ",
    "справочник зоуит",
    "ЗОУИТ",
    "зоуит"
]

for text in test_texts:
    text_lower = text.lower()
    match = 'справочник' in text_lower or 'зоуит' in text_lower
    result = "✅" if match else "❌"
    print(f"  {result} '{text}': {match}")

# Тест 3: Кадастровые номера
print("\n📝 Тест 3: Кадастровые номера")
import re

# Кадастровый паттерн с экранированным бэкслэшем
cadastral_pattern = r'\\d{2}:\\d{2}:\\d{7}:\\d+'

test_cadastral = [
    "77:06:0009004:229",
    "50:01:0000000:123",
    "не кадастровый"
]

for text in test_cadastral:
    match = re.search(cadastral_pattern, text)
    result = "✅" if match else "❌"
    print(f"  {result} '{text}': {bool(match)}")

print("\n🎉 Тестирование завершено!")
