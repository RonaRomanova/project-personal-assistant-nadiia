from cli import (
    parse_input,
    add_contact,
    edit_phone,
    edit_email, 
    edit_address,
    edit_birthday,
    find_contact,
    delete_contact,
    show_all,
    birthdays,
)
from storage import load_data, save_data


def main() -> None:
    """
    Основний цикл роботи бота.
    """
    book = load_data()
    print(" \nПривіт. Я — Personal Assistant 'NADIIA2'!\n\n" \
          
          "Я не зміню твоє життя за 3 секунди, не пообіцяю “AI magic” і не буду вдавати з себе iPhone 27 Pro Max.\n" \
          "Я просто допоможу тобі з організацією твоїх контактів, введи 'help' щоб побачити всі доступні команди.")

    while True:
        user_input = input("\n >>>>>> Введіть команду: ")
        command, args, kwargs = parse_input(user_input)

        if command in ["close", "exit"]:
            print("До побачення!")
            break

        elif command == "hello":
            print("Як я можу вам допомогти?")
        
        elif command == "help":
            print("Доступні команди:\n \n" \
                " - add: Додає новий контакт. Формат: add 'Elon Musk' 0991234999 email=asd@example.com email=asd@example.co birthday=15.03.1971 address='Mars'\n" \
                " - edit-phone: Редагує номер телефону контакту. Формат: edit-phone 'Elon Musk' +380991234999 +380991234998\n" \
                " - edit-email: Редагує email контакту. Формат: edit-email 'Elon Musk' asd@example.com new@example.com\n" \
                " - edit-address: Редагує адресу контакту. Формат: edit-address 'Elon Musk' 'New Address'\n" \
                " - edit-birthday: Редагує день народження контакту. Формат: edit-birthday 'Elon Musk' 15.03.1971\n" \
                " - all: Показує всі контакти. Формат: all\n" \
                " - birthdays: Показує список найближчих днів народження. Формат: birthdays\n" \
                " - find: Знаходить контакт за ім'ям, телефоном або адресою. Формат: find 'Elon Musk' phone=+380991234999 email=asd@example.com address='Mars'\n" \
                " - delete: Видаляє контакт за ім'ям. Формат: delete 'Elon Musk'\n" \
                " - help: Показує це повідомлення. Формат: help\n" \
                " - close/exit: Завершує роботу бота. Формат: close або exit" )

        elif command == "add":
            print(add_contact(args, book, **kwargs))
            save_data(book)

        elif command == "edit-phone":
            print(edit_phone(args, book, **kwargs))
            save_data(book)

        elif command == "edit-email":
            print(edit_email(args, book, **kwargs))
            save_data(book)

        elif command == "edit-birthday":
            print(edit_birthday(args, book, **kwargs))
            save_data(book)

        elif command == "edit-address":
            print(edit_address(args, book, **kwargs))
            save_data(book)

        elif command == "all":
            print(show_all(book, **kwargs))

        elif command == "birthdays":
            print(birthdays(args, book, **kwargs))

        elif command == "find":
            print(find_contact(args, book))

        elif command == "delete":
            print(delete_contact(args, book))

        else:
            print("Невірна команда.")

if __name__ == "__main__":
    main()