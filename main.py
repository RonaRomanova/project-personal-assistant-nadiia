from rich import print
from rich.console import Console

from cli import (
    add_contact,
    add_note,  # додано для нотаток
    all_notes,  # додано для нотаток
    birthdays,
    delete_contact,
    delete_note,  # додано для нотаток
    edit_address,
    edit_birthday,
    edit_email,
    edit_note,  # додано для нотаток
    edit_phone,
    edit_tag,  # додано для нотаток
    find_contact,
    find_note,  # додано для нотаток
    parse_input,
    show_all,
)
from storage import load_book, load_notes, save_book, save_notes
from utils.helpers import print_ukrainian_flag

console = Console()


def main() -> None:
    """
    Основний цикл роботи бота.
    """
    book = load_book()
    notes = load_notes()

    print_ukrainian_flag()

    print(
        "Привіт. Я — Personal Assistant "
        "[bold magenta]NADIIA2[/bold magenta] 🦄!\n\n"
        "Я не зміню твоє життя за 3 секунди, "
        "не пообіцяю “AI magic” і не буду вдавати з себе "
        "🍎 [i cyan]iPhone 27 Pro Max[/i cyan].\n"
        "Я просто допоможу тобі з організацією "
        "твоїх контактів, введи 'help' щоб побачити "
        "всі доступні команди."
    )

    while True:
        user_input = console.input(
            "\n [bold magenta]>>>>>> Введіть команду:[/bold magenta] "
        )
        command, args, kwargs = parse_input(user_input)

        if command in ["close", "exit"]:
            print("До побачення!")
            break

        elif command == "hello":
            print("Як я можу вам допомогти?")

        elif command == "help":
            print(
                "Доступні команди:\n \n"
                " - add: Додає новий контакт. Формат:\n"
                "   add 'Elon Musk' 0991234999 "
                "email=asd@example.com birthday=15.03.1971\n"
                " - edit-phone: Редагує номер телефону контакту. "
                "Формат: edit-phone 'Elon Musk' "
                "+380991234999 +380991234998\n"
                " - edit-email: Редагує email контакту. "
                "Формат: edit-email 'Elon Musk' old@e.com new@e.com\n"
                " - edit-address: Редагує адресу контакту. "
                "Формат: edit-address 'Elon Musk' 'New Address'\n"
                " - edit-birthday: Редагує день народження контакту. "
                "Формат: edit-birthday 'E' 15.03.1971\n"
                " - all: Показує всі контакти. Формат: all\n"
                " - birthdays: Показує найближчі дні народження. "
                "Формат: birthdays\n"
                " - find: Знаходить контакт за ім'ям, телефоном "
                "або адресою. Формат: find 'Elon Musk' "
                "phone=+380991234999 email=asd@example.com\n"
                " - delete: Видаляє контакт за ім'ям. "
                "Формат: delete 'Elon Musk'\n"
                " - help: Показує це повідомлення. Формат: help\n"
                " - add-note: Додає нотатку. Формат: add-note "
                '"text" [tag1 tag2 ...]\n'
                " - edit-note: Редагує нотатку. Формат: "
                'edit-note <ID> "new text"\n'
                " - edit-tag: Редагує теги. Формат: edit-tag "
                "<ID> add <tag1> [tag2...] або edit-tag <ID> "
                "delete <tag>\n"
                " - delete-note: Видаляє нотатку. "
                "Формат: delete-note <ID>\n"
                " - find-note: Шукає нотатки. Формат: "
                "find-note <query>\n"
                " - all-notes: Показує всі нотатки. "
                "Формат: all-notes\n"
                " - close/exit: Завершує роботу бота. "
                "Формат: close або exit"
            )

        elif command == "add":
            print(add_contact(args, book, **kwargs))
            save_book(book)

        elif command == "edit-phone":
            print(edit_phone(args, book, **kwargs))
            save_book(book)

        elif command == "edit-email":
            print(edit_email(args, book, **kwargs))
            save_book(book)

        elif command == "edit-birthday":
            print(edit_birthday(args, book, **kwargs))
            save_book(book)

        elif command == "edit-address":
            print(edit_address(args, book, **kwargs))
            save_book(book)

        elif command == "all":
            print(show_all(book, **kwargs))

        elif command == "birthdays":
            print(birthdays(args, book, **kwargs))

        elif command == "find":
            print(find_contact(args, book))

        elif command == "delete":
            print(delete_contact(args, book))
            save_book(book)

        # Додайте обробку нотаток, якщо потрібно
        elif command == "add-note":
            print(add_note(args, notes))
            save_notes(notes)

        elif command == "edit-note":
            print(edit_note(args, notes))
            save_notes(notes)

        elif command == "edit-tag":
            print(edit_tag(args, notes))
            save_notes(notes)

        elif command == "delete-note":
            print(delete_note(args, notes))
            save_notes(notes)

        elif command == "find-note":
            print(find_note(args, notes))

        elif command == "all-notes":
            print(all_notes(notes))

        else:
            print("Невірна команда.")


if __name__ == "__main__":
    main()
