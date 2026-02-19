import json
import urllib.parse
import socket

def get_server_ip():
    """Получает внешний IP адрес сервера"""
    try:
        # Создаем временное соединение чтобы определить внешний IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Не обязательно подключаться, просто получаем адрес
        s.connect(("8.8.8.8", 80))
        ip_address = s.getsockname()[0]
        s.close()
        return ip_address
    except:
        # Если не получилось, попробуем через hostname
        try:
            hostname = socket.gethostname()
            return socket.gethostbyname(hostname)
        except:
            return None

def generate_user_url(name, user_metadata_file='user_metadata.json'):
    # Загружаем данные
    with open(user_metadata_file, 'r') as f:
        metadata = json.load(f)

    # Ищем пользователя по имени
    user_data = None
    for user_id, user_info in metadata['users'].items():
        if user_info['name'] == name:
            user_data = user_info
            break

    if not user_data:
        print(f"Пользователь с именем '{name}' не найден")
        return None

    # Получаем данные сервера
    server = metadata['server']
    server_name = server['serverName']  # Это для SNI (должно быть vk.com)
    port = server['port']

    # Получаем IP адрес сервера
    server_ip = get_server_ip()
    if not server_ip:
        print("Не удалось определить IP адрес сервера")
        return None

    # Получаем данные пользователя
    uuid = user_data['data']['id']
    short_id = user_data['shortId']
    flow = user_data['data']['flow']

    # Формируем параметры запроса
    params = {
        'type': 'tcp',
        'headerType': 'none',
        'flow': flow,
        'security': 'reality',
        'sni': server_name,  # SNI остаётся vk.com
        'pbk': server['publicKey'],
        'sid': short_id,
        'fp': 'randomized'
    }

    # Кодируем параметры
    query_string = urllib.parse.urlencode(params)

    # Формируем URL с IP адресом сервера
    url = f"vless://{uuid}@{server_ip}:{port}?{query_string}#{urllib.parse.quote(name)}"

    return url

def get_user_url(name):
    url = generate_user_url(name)
    if url:
        print(f"URL для пользователя '{name}':")
        print(url)
    return url

# Использование
# get_user_url("имя_пользователя")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        get_user_url(sys.argv[1])
    else:
        name = input("Введите имя пользователя: ")
        get_user_url(name)
