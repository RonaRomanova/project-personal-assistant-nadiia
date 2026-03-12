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
    print("Ласкаво просимо в помічника бота!")

    while True:
        user_input = input("\n >>>>>> Введіть команду: ")
        command, args, kwargs = parse_input(user_input)

        if command in ["close", "exit"]:
            print("До побачення!")
            break

        elif command == "hello":
            print("Як я можу вам допомогти?")

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