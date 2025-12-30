# Инструкция по развертыванию бота на Railway.app

## Шаг 1: Регистрация
1. Перейдите на https://railway.app
2. Нажмите "Login" и войдите через GitHub
3. Разрешите доступ к репозиториям

## Шаг 2: Создание проекта
1. Нажмите "New Project"
2. Выберите "Deploy from GitHub repo"
3. Найдите и выберите `cuzemlya-wq/zemlya-bot-vk`
4. Нажмите "Deploy Now"

## Шаг 3: Настройка переменных окружения
1. Откройте ваш проект
2. Перейдите в "Variables"
3. Добавьте следующие переменные:

```
VK_TOKEN=vk1.a.b8ph5kZ8RxyeQ1nU7EJRksuTyT8cQSZmDcz50jO7QHla3WdUXZRBoWH64MTU-2EjnmFLDsD_cWEi4FD0lQ6cQYWuVpZoOmGfTTCBagcxECU66efIpMxh-XlXK9866gKFl4sf2LQhkWKHu7R13HnejW86LXSZAkU10uKjiaU8pn00O_m0ySgiTJAL3hamhfkGphuoxa8k6dzY2QmVPntg0Q
VK_GROUP_ID=234842494
```

## Шаг 4: Проверка работы
1. Railway автоматически установит зависимости из `requirements.txt`
2. Запустит бота согласно `Procfile`
3. Проверьте логи в разделе "Deployments"
4. Отправьте тестовое сообщение боту в VK

## Важно:
- Бесплатный план: 500 часов в месяц
- Бот работает 24/7 в пределах лимита
- Автоматический редеплой при push в GitHub
