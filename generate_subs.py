import json
import base64
import os
import secrets
from get_url import generate_user_url
from settings import USER_METADATA_FILE, SUBS_DIRECTORY

def update_subscription(name, user_metadata_file=USER_METADATA_FILE):
    if not os.path.exists(SUBS_DIRECTORY):
        os.makedirs(SUBS_DIRECTORY, exist_ok=True)

    with open(user_metadata_file, 'r') as f:
        metadata = json.load(f)

    # Ищем UUID пользователя
    user_uuid = next((uid for uid, info in metadata['users'].items() if info['name'] == name), None)
    if not user_uuid:
        return None

    # Генерируем или берем имя файла
    sub_filename = metadata['users'][user_uuid].get('sub_filename')
    if not sub_filename:
        sub_filename = f"sub_{secrets.token_hex(8)}.txt"
        metadata['users'][user_uuid]['sub_filename'] = sub_filename
        with open(user_metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)

    # Генерируем контент (VLESS -> Base64)
    url = generate_user_url(name, user_metadata_file)
    if url:
        sub_content = base64.b64encode(url.encode('utf-8')).decode('utf-8')
        file_path = os.path.join(SUBS_DIRECTORY, sub_filename)
        with open(file_path, 'w') as f:
            f.write(sub_content)
        return sub_filename
    return None

def delete_subscription_file(sub_filename):
    """Удаляет файл подписки с диска"""
    if sub_filename:
        file_path = os.path.join(SUBS_DIRECTORY, sub_filename)
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"Файл подписки {sub_filename} удален.")

def update_all_subs(user_metadata_file='user_metadata.json'):
    """Обновляет файлы для всех существующих пользователей"""
    try:
        with open(user_metadata_file, 'r') as f:
            metadata = json.load(f)

        for user_info in metadata['users'].values():
            name = user_info['name']
            update_subscription(name, user_metadata_file)
        print("Все файлы подписок успешно синхронизированы.")
    except Exception as e:
        print(f"Ошибка при массовом обновлении: {e}")
