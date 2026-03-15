from rich import print
from rich.console import Console

import cli
from cli.constants import (
    WELCOME_MSG,
    EXIT_MSG,
    HELP_TEXT,
    HELP_PROMPT,
    UNKNOWN_COMMAND,
)
from storage import load_book, load_notes, save_book, save_notes
from utils.helpers import print_ukrainian_flag

console = Console()


def main() -> None:
    """Основний цикл роботи бота."""
    book = load_book()
    notes = load_notes()

    print_ukrainian_flag()
    print(WELCOME_MSG)

    # Диспетчер команд
    commands = {
        "add": lambda a, k: (console.print(cli.add_contact(a, book, **k)),
                             save_book(book)),
        "edit-phone": lambda a, k: (console.print(cli.edit_phone(a, book, **k)),
                                    save_book(book)),
        "edit-email": lambda a, k: (console.print(cli.edit_email(a, book, **k)),
                                    save_book(book)),
        "edit-birthday": lambda a, k: (console.print(cli.edit_birthday(a, book, **k)),
                                       save_book(book)),
        "edit-address": lambda a, k: (console.print(cli.edit_address(a, book, **k)),
                                      save_book(book)),
        "all": lambda a, k: console.print(cli.show_all(book, **k)),
        "birthdays": lambda a, k: console.print(cli.birthdays(a, book, **k)),
        "find": lambda a, k: console.print(cli.find_contact(a, book)),
        "delete": lambda a, k: (console.print(cli.delete_contact(a, book)),
                                save_book(book)),
        "add-note": lambda a, k: (console.print(cli.add_note(a, notes)),
                                  save_notes(notes)),
        "edit-note": lambda a, k: (console.print(cli.edit_note(a, notes)),
                                   save_notes(notes)),
        "edit-tag": lambda a, k: (console.print(cli.edit_tag(a, notes)),
                                  save_notes(notes)),
        "delete-note": lambda a, k: (console.print(cli.delete_note(a, notes)),
                                     save_notes(notes)),
        "find-note": lambda a, k: console.print(cli.find_note(a, notes)),
        "all-notes": lambda a, k: console.print(cli.all_notes(notes)),
        "hello": lambda a, k: print("Як я можу вам допомогти?"),
        "help": lambda a, k: print(HELP_TEXT),
    }

    while True:
        user_input = console.input(HELP_PROMPT)
        command, args, kwargs = cli.parse_input(user_input)

        if command in ["close", "exit"]:
            print(EXIT_MSG)
            break

        if command in commands:
            commands[command](args, kwargs)
        else:
            print(UNKNOWN_COMMAND)


if __name__ == "__main__":
    main()
