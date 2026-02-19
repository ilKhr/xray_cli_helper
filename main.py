import sys
import json
# Импортируем всё необходимое сразу
from add_user import add_user
from remove_user import remove_user_by_name
from get_url import get_user_url, get_server_ip
from generate_subs import update_all_subs
from settings import USER_METADATA_FILE, SUBS_PORT

def main():
    print("\n--- Xray User Manager ---")
    print("1. Добавить пользователя")
    print("2. Удалить пользователя")
    print("3. Получить URL пользователя")
    print("4. Обновить все файлы подписок")
    print("5. Выйти")

    choice = input("Выберите действие: ")

    if choice == '1':
        name = input("Введите имя нового пользователя: ")
        add_user(name)

    elif choice == '2':
        name = input("Введите имя пользователя для удаления: ")
        remove_user_by_name(name)

    elif choice == '3':
        name = input("Введите имя пользователя: ")
        url = get_user_url(name)

        if url:
            # Читаем метаданные для получения имени файла подписки
            try:
                with open(USER_METADATA_FILE, 'r') as f:
                    meta = json.load(f)

                # Ищем инфо о файле подписки
                sub_file = None
                for info in meta['users'].values():
                    if info['name'] == name:
                        sub_file = info.get('sub_filename')
                        break

                if sub_file:
                    ip = get_server_ip()
                    print(f"Ссылка на подписку: http://{ip}:{SUBS_PORT}/xraysubs/{sub_file}")
                else:
                    print("Файл подписки еще не создан для этого пользователя.")
            except FileNotFoundError:
                print("Ошибка: файл user_metadata.json не найден.")

    elif choice == '4':
        update_all_subs()
        print("Все файлы подписок обновлены на диске.")

    elif choice == '5':
        print("Выход...")
        sys.exit()
    else:
        print("Неверный выбор, попробуйте снова.")

if __name__ == "__main__":
    while True:
        try:
            main()
        except KeyboardInterrupt:
            print("\nПрервано пользователем.")
            sys.exit()
