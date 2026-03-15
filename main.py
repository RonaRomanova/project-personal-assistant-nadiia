from rich import print
from rich.console import Console

import questionary
from prompt_toolkit.completion import WordCompleter, ConditionalCompleter
from prompt_toolkit.shortcuts import CompleteStyle
from prompt_toolkit.filters import Condition
from prompt_toolkit.application import get_app
from prompt_toolkit.history import FileHistory

import cli
from cli.constants import (
    WELCOME_MSG,
    EXIT_MSG,
    HELP_TEXT,
    HELP_PROMPT,
    HOW_CAN_I_HELP,
    UNKNOWN_COMMAND,
)
from storage import load_book, load_notes, save_book, save_notes
from utils.helpers import print_ukrainian_flag

console = Console()


def main() -> None:
    """Основний цикл роботи бота."""
    book = load_book()
    notes = load_notes()
    history = FileHistory(".history")

    print_ukrainian_flag()
    print(WELCOME_MSG)

    # Диспетчер команд
    commands = {
        "add-contact": lambda a, k: (console.print(cli.add_contact(a, book, **k)),
                             save_book(book)),
        "edit-phone": lambda a, k: (console.print(cli.edit_phone(a, book, **k)),
                                    save_book(book)),
        "edit-email": lambda a, k: (console.print(cli.edit_email(a, book, **k)),
                                    save_book(book)),
        "edit-birthday": lambda a, k: (console.print(cli.edit_birthday(a, book, **k)),
                                       save_book(book)),
        "edit-address": lambda a, k: (console.print(cli.edit_address(a, book, **k)),
                                      save_book(book)),
        "all-contacts": lambda a, k: console.print(cli.show_all(book, **k)),
        "birthdays": lambda a, k: console.print(cli.birthdays(a, book, **k)),
        "find-contact": lambda a, k: console.print(cli.find_contact(a, book)),
        "delete-contact": lambda a, k: (console.print(cli.delete_contact(a, book)),
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
        "hello": lambda a, k: print(HOW_CAN_I_HELP),
        "help": lambda a, k: print(HELP_TEXT),
    }

    # Список команд для автозаповнення
    command_list = list(commands.keys()) + ["close", "exit"]
    word_completer = WordCompleter(command_list, ignore_case=True)

    @Condition
    def is_not_after_space():
        """Повертає True, якщо в рядку ще немає пробілів."""
        buffer = get_app().current_buffer
        return " " not in buffer.text

    completer = ConditionalCompleter(word_completer, is_not_after_space)

    # Стиль для questionary
    style = questionary.Style([
        ('question', 'fg:magenta bold'),
        ('answer', 'fg:white'),
    ])

    while True:
        try:
            # Використовуємо questionary для вводу з автодоповненням
            user_input = questionary.text(
                HELP_PROMPT,
                completer=completer,
                history=history,
                qmark="",
                style=style,
                complete_style=CompleteStyle.COLUMN
            ).ask()

            if user_input is None:
                break

            command, args, kwargs = cli.parse_input(user_input)

            if command in ["close", "exit"]:
                print(EXIT_MSG)
                break

            if command in commands:
                commands[command](args, kwargs)
            else:
                print(UNKNOWN_COMMAND)
        except KeyboardInterrupt:
            print(EXIT_MSG)
            break


if __name__ == "__main__":
    main()
