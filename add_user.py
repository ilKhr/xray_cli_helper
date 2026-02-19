import json
import uuid
import secrets
from generate_subs import update_subscription
from settings import USER_METADATA_FILE, XRAY_CONFIG_FILE

def add_user(name, user_metadata_file=USER_METADATA_FILE, config_file=XRAY_CONFIG_FILE):
    # Загружаем существующие данные
    with open(user_metadata_file, 'r') as f:
        metadata = json.load(f)

    with open(config_file, 'r') as f:
        config = json.load(f)

    # Генерируем новый UUID
    new_uuid = str(uuid.uuid4())

    # Генерируем новый shortId (8 байт в hex)
    new_short_id = secrets.token_hex(8)

    # Добавляем в user_metadata
    metadata['users'][new_uuid] = {
        "name": name,
        "data": {
            "id": new_uuid,
            "flow": "xtls-rprx-vision"
        },
        "shortId": new_short_id
    }

    # Добавляем shortId в список сервера
    metadata['server']['shortIds'].append(new_short_id)

    # Добавляем клиента в config.json
    new_client = {
        "id": new_uuid,
        "flow": "xtls-rprx-vision"
    }
    config['inbounds'][0]['settings']['clients'].append(new_client)

    # Добавляем shortId в realitySettings
    config['inbounds'][0]['streamSettings']['realitySettings']['shortIds'].append(new_short_id)

    # Сохраняем изменения
    with open(user_metadata_file, 'w') as f:
        json.dump(metadata, f, indent=2)

    with open(config_file, 'w') as f:
        json.dump(config, f, indent=2)

    print(f"Пользователь '{name}' добавлен!")
    print(f"UUID: {new_uuid}")
    print(f"ShortId: {new_short_id}")

    sub_file = update_subscription(name, user_metadata_file)
    print(f"Файл подписки создан: {sub_file}")

    return new_uuid, new_short_id

# Использование
# add_user("новый_пользователь")
