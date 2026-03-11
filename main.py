from cli import (
    parse_input,
    add_contact,
    change_contact,
    show_phone,
    show_all,
    add_birthday,
    show_birthday,
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
        user_input = input("Введіть команду: ")
        command, args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("До побачення!")
            break

        elif command == "hello":
            print("Як я можу вам допомогти?")

        elif command == "add":
            print(add_contact(args, book))
            save_data(book)

        elif command == "change":
            print(change_contact(args, book))
            save_data(book)

        elif command == "phone":
            print(show_phone(args, book))

        elif command == "all":
            print(show_all(book))

        elif command == "add-birthday":
            print(add_birthday(args, book))
            save_data(book)

        elif command == "show-birthday":
            print(show_birthday(args, book))

        elif command == "birthdays":
            print(birthdays(args, book))

        else:
            print("Невірна команда.")


if __name__ == "__main__":
    main()