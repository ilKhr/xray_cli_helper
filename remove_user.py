import json
import os
from generate_subs import delete_subscription_file
from settings import USER_METADATA_FILE, XRAY_CONFIG_FILE

def remove_user_by_name(name, user_metadata_file=USER_METADATA_FILE, config_file=XRAY_CONFIG_FILE):
    with open(user_metadata_file, 'r') as f:
        metadata = json.load(f)
    with open(config_file, 'r') as f:
        config = json.load(f)

    user_to_remove = None
    sub_filename_to_delete = None

    for user_id, user_data in metadata['users'].items():
        if user_data['name'] == name:
            user_to_remove = user_id
            user_short_id = user_data['shortId']
            # Запоминаем имя файла перед удалением записи
            sub_filename_to_delete = user_data.get('sub_filename')
            break

    if not user_to_remove:
        print(f"Пользователь с именем '{name}' не найден")
        return False

    # 1. Удаляем физический файл подписки
    if sub_filename_to_delete:
        delete_subscription_file(sub_filename_to_delete)

    # 2. Удаляем из метаданных
    del metadata['users'][user_to_remove]
    if user_short_id in metadata['server']['shortIds']:
        metadata['server']['shortIds'].remove(user_short_id)

    # 3. Удаляем из конфига Xray
    config['inbounds'][0]['settings']['clients'] = [
        c for c in config['inbounds'][0]['settings']['clients'] if c['id'] != user_to_remove
    ]
    config['inbounds'][0]['streamSettings']['realitySettings']['shortIds'] = [
        sid for sid in config['inbounds'][0]['streamSettings']['realitySettings']['shortIds'] if sid != user_short_id
    ]

    # Сохраняем
    with open(user_metadata_file, 'w') as f:
        json.dump(metadata, f, indent=2)
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=2)

    print(f"Пользователь '{name}' полностью удален.")
    return True
