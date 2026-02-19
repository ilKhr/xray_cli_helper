import json

def remove_user_by_name(name, user_metadata_file='user_metadata.json', config_file='config.json'):
    # Загружаем данные
    with open(user_metadata_file, 'r') as f:
        metadata = json.load(f)

    with open(config_file, 'r') as f:
        config = json.load(f)

    # Ищем пользователя по имени
    user_to_remove = None
    user_uuid = None
    user_short_id = None

    for user_id, user_data in metadata['users'].items():
        if user_data['name'] == name:
            user_to_remove = user_id
            user_short_id = user_data['shortId']
            break

    if not user_to_remove:
        print(f"Пользователь с именем '{name}' не найден")
        return False

    # Удаляем из user_metadata
    del metadata['users'][user_to_remove]

    # Удаляем shortId из списка сервера
    if user_short_id in metadata['server']['shortIds']:
        metadata['server']['shortIds'].remove(user_short_id)

    # Удаляем клиента из config.json
    clients = config['inbounds'][0]['settings']['clients']
    config['inbounds'][0]['settings']['clients'] = [
        client for client in clients if client['id'] != user_to_remove
    ]

    # Удаляем shortId из realitySettings
    short_ids = config['inbounds'][0]['streamSettings']['realitySettings']['shortIds']
    config['inbounds'][0]['streamSettings']['realitySettings']['shortIds'] = [
        sid for sid in short_ids if sid != user_short_id
    ]

    # Сохраняем изменения
    with open(user_metadata_file, 'w') as f:
        json.dump(metadata, f, indent=2)

    with open(config_file, 'w') as f:
        json.dump(config, f, indent=2)

    print(f"Пользователь '{name}' удален!")
    return True

# Использование
# remove_user_by_name("имя_пользователя")
