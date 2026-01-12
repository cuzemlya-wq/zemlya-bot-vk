#!/bin/bash
echo '🔄 Обновление бота...'

# Остановка бота
echo '⚠️ Останавливаю старый процесс...'
pkill -f 'python.*bot_main'
sleep 2

# Обновление кода
echo '📥 Загружаю новый код...'
git fetch origin
git reset --hard origin/main

echo '✅ Код обновлен!'

# Перезапуск бота
echo '🚀 Запускаю бота...'
nohup python3 -m src.bot_main > bot.log 2>&1 &

echo '✅ Бот запущен! PID:' $!
echo '📜 Логи: tail -f bot.log'
