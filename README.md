# Xray User Manager (CLI + Subscriptions)

Легковесный Python-инструментарий для управления пользователями VLESS-Reality-Vision и автоматической генерации статических подписок.

## ⚠️ Ключевая особенность

Генерация ссылок и подписок происходит на основе данных из `user_metadata.json`, **а не путем парсинга рабочего конфига Xray**. Это позволяет:

- Хранить кастомные имена пользователей (которых нет в `config.json`)
- Массово обновлять ссылки при смене IP/порта сервера без ручной правки каждого клиента
- Использовать постоянные UUID и ShortId даже при перегенерации основного конфига

## Архитектура

- **`main.py`**: Интерактивное CLI-меню
- **`add_user.py` / `remove_user.py`**: Синхронная модификация `config.json` (Xray) и `user_metadata.json`
- **`generate_subs.py`**: Кодирование ссылок в Base64 и сохранение в `/var/www/html/xraysubs/`
- **`settings.py`**: Загрузка путей и параметров из `.env`

## Быстрый старт

### 1. Установка зависимостей

```bash
pip install python-dotenv
```

### 2. Настройка окружения (.env)

Создайте файл `.env` в корне проекта (он игнорируется Git):

```env
PROJECT_ROOT=/home/user/xray_manager
USER_METADATA_FILE=/home/user/xray_manager/user_metadata.json
XRAY_CONFIG_FILE=/usr/local/etc/xray/config.json
SUBS_DIRECTORY=/var/www/html/xraysubs
SUBS_URL_PATH=xraysubs
```

### 3. Права доступа

Убедитесь, что у пользователя есть права на запись в папку веб-сервера:

```bash
sudo chown -R $USER:$USER /var/www/html/xraysubs
```

### 4. Запуск

```bash
python3 main.py
```

## Формат подписки

Скрипт генерирует файлы с обфусцированными именами (например, `sub_a1b2c3d4.txt`). Пользователь добавляет в клиент ссылку вида:

```
http://SERVER_IP/xraysubs/sub_a1b2c3d4.txt
```

При удалении пользователя через меню файл подписки автоматически удаляется с сервера.
