import os
from dotenv import load_dotenv

# Загружаем переменные из .env
load_dotenv()

print(f"DEBUG: Путь из env: {os.getenv('USER_METADATA_FILE')}")

# Вспомогательная функция для получения путей
def get_env(key, default=None):
    return os.getenv(key, default)

# Пути к файлам (приоритет .env -> потом дефолт)
PROJECT_ROOT = get_env('PROJECT_ROOT', os.path.dirname(os.path.abspath(__file__)))
USER_METADATA_FILE = get_env('USER_METADATA_FILE', os.path.join(PROJECT_ROOT, 'user_metadata.json'))
XRAY_CONFIG_FILE = get_env('XRAY_CONFIG_FILE', os.path.join(PROJECT_ROOT, 'config.json'))

# Настройки подписок
SUBS_DIRECTORY = get_env('SUBS_DIRECTORY', '/var/www/html/xraysubs')

# Проверка папки подписок
if not os.path.exists(SUBS_DIRECTORY):
    try:
        os.makedirs(SUBS_DIRECTORY, exist_ok=True)
    except PermissionError:
        pass # Права проверим при записи
