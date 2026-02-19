import sys

def main():
    print("Xray User Manager")
    print("1. Добавить пользователя")
    print("2. Удалить пользователя")
    print("3. Получить URL пользователя")
    print("4. Выйти")

    choice = input("Выберите действие: ")

    if choice == '1':
        name = input("Введите имя нового пользователя: ")
        add_user(name)

    elif choice == '2':
        name = input("Введите имя пользователя для удаления: ")
        remove_user_by_name(name)

    elif choice == '3':
        name = input("Введите имя пользователя: ")
        get_user_url(name)

    elif choice == '4':
        sys.exit()
    else:
        print("Неверный выбор")

if __name__ == "__main__":
    # Импортируем все функции
    from add_user import add_user
    from remove_user import remove_user_by_name
    from get_url import get_user_url

    while True:
        main()
