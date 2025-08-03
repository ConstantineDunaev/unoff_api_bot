# Telegram бот для автоматизации задач в личном кабинете продавца Wildberries

## Функционал:
- Добавление и обновление личных кабинетов WB;
- Возможность ручного запуска функциональных скриптов через inline меню Telegram бота;
- Возможность автоматического запуска функциональных скриптов посредством cron;
- Сохранение данных о скидке WB в таблицу базы данных MySQL.

## Требования:
- Python 3.11+
- MySQL 5.7+

## Переменные окружения:
- `TELEGRAM_TOKEN` - токен Telegram бота;
- `TELEGRAM_USERS` - список Telegram User ID через запятую, для доступа к функционалу бота;
- `MYSQL_HOST` - сервер MySQL;
- `MYSQL_USER` - пользователь MySQL;
- `MYSQL_PASSWORD` - пароль MySQL;
- `MYSQL_PORT` - порт MySQL;
- `MYSQL_SCHEMA` - название базы данных MySQL;
- `MYSQL_DUMP` - путь к дампу таблиц MySQL.

Поддерживается загрузка переменных окружения из файла `.env`.

## Установка и запуск:
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
chmod +x create_service.sh
./create_service.sh
```

### Управление процессом systemd
Остановка:
```
systemctl stop unoff_api_bot
```

Перезапуск:
```
systemctl restart unoff_api_bot
```

### Автоматизированный запуск cron:
Для автоматического выполнения необходимого функционального скрипта необходимо добавить в cron:
```
0 6 * * * /root/unoff_api_bot/venv/bin/python /root/unoff_api_bot/cron.py discount_wb
```