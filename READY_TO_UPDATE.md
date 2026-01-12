# 🚀 БОТ ГОТОВ К ОБНОВЛЕНИЮ!

## ✅ ВСЁ ГОТОВО

Исправлена ошибка, код запушен в GitHub.

---

## 🔑 ВАШ СЕРВЕР TIMEWEB

**IP:** 147.45.154.133

**Подключитесь по SSH:**

```bash
ssh root@147.45.154.133
```

---

## ⚡ КОМАНДЫ ДЛЯ ОБНОВЛЕНИЯ

### Вариант 1: Автоматический (рекомендуется)

```bash
# После подключения:
cd /root/zemlya-bot-vk  # или ваш путь
./UPDATE_BOT.sh
```

### Вариант 2: Если не знаете путь

```bash
# 1. Найти бота
ps aux | grep bot_main
find / -name "zemlya-bot-vk" -type d 2>/dev/null

# 2. Остановить
pkill -f 'python.*bot_main'

# 3. Перейти в папку
cd <путь-к-боту>

# 4. Обновить код
git fetch origin
git reset --hard origin/main

# 5. Запустить
nohup python3 -m src.bot_main > bot.log 2>&1 &

# 6. Проверить
tail -f bot.log
```

---

## ✅ ПРОВЕРКА РАБОТЫ

Отправьте в VK боту:

**"Справочник ЗОУИТ"**

Бот должен ответить со справочником! ✅

---

## 📌 ССЫЛКИ

- Timeweb: https://timeweb.cloud/my/servers/6328415
- GitHub: https://github.com/cuzemlya-wq/zemlya-bot-vk
- VK бот: https://vk.com/im/convo/-234842494

---

🔥 **ВСЁ ГОТОВО! ОСТАЛОСЬ ТОЛЬКО ПОДКЛЮЧИТЬСЯ ПО SSH И ОБНОВИТЬ!**
