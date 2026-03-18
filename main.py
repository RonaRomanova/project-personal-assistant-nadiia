import questionary
from prompt_toolkit.application import get_app
from prompt_toolkit.completion import ConditionalCompleter, WordCompleter
from prompt_toolkit.filters import Condition
from prompt_toolkit.history import FileHistory
from prompt_toolkit.shortcuts import CompleteStyle
from rich import print
from rich.console import Console

import cli
from cli.constants import (
    AUTOCOMPLETE_PATTERN,
    EXIT_MSG,
    HELP_PROMPT,
    HELP_TEXT,
    HOW_CAN_I_HELP,
    UNKNOWN_COMMAND,
    WELCOME_MSG,
)
from storage import (
    get_storage_info,
    load_book,
    load_notes,
    save_book,
    save_notes,
)
from utils import print_ukrainian_flag, setup_logger

console = Console()
logger = setup_logger()


def main() -> None:
    """Основний цикл роботи бота."""
    logger.info("Application started")
    book = load_book()
    notes = load_notes()
    history = FileHistory(".history")

    print_ukrainian_flag()
    print(WELCOME_MSG)

    # Диспетчер команд
    commands = {
        "add-contact": lambda a, k: (
            console.print(cli.add_contact(a, book, **k)),
            save_book(book),
        ),
        "edit-phone": lambda a, k: (
            console.print(cli.edit_phone(a, book, **k)),
            save_book(book),
        ),
        "edit-email": lambda a, k: (
            console.print(cli.edit_email(a, book, **k)),
            save_book(book),
        ),
        "edit-birthday": lambda a, k: (
            console.print(cli.edit_birthday(a, book, **k)),
            save_book(book),
        ),
        "edit-address": lambda a, k: (
            console.print(cli.edit_address(a, book, **k)),
            save_book(book),
        ),
        "all-contacts": lambda a, k: console.print(cli.show_all(book, **k)),
        "birthdays": lambda a, k: console.print(cli.birthdays(a, book, **k)),
        "find-contact": lambda a, k: console.print(cli.find_contact(a, book)),
        "delete-contact": lambda a, k: (
            console.print(cli.delete_contact(a, book)),
            save_book(book),
        ),
        "add-note": lambda a, k: (
            console.print(cli.add_note(a, notes)),
            save_notes(notes),
        ),
        "edit-note": lambda a, k: (
            console.print(cli.edit_note(a, notes)),
            save_notes(notes),
        ),
        "edit-tag": lambda a, k: (
            console.print(cli.edit_tag(a, notes)),
            save_notes(notes),
        ),
        "delete-note": lambda a, k: (
            console.print(cli.delete_note(a, notes)),
            save_notes(notes),
        ),
        "find-note": lambda a, k: console.print(cli.find_note(a, notes)),
        "all-notes": lambda a, k: console.print(cli.all_notes(notes)),
        "hello": lambda a, k: print(HOW_CAN_I_HELP),
        "help": lambda a, k: print(HELP_TEXT),
    }

    # Список команд для автозаповнення
    command_list = list(commands.keys()) + ["close", "exit"]
    word_completer = WordCompleter(
        command_list, ignore_case=True, pattern=AUTOCOMPLETE_PATTERN
    )

    @Condition
    def is_not_after_space():
        """Повертає True, якщо в рядку ще немає пробілів."""
        buffer = get_app().current_buffer
        return " " not in buffer.text

    completer = ConditionalCompleter(word_completer, is_not_after_space)

    # Стиль для questionary
    style = questionary.Style(
        [
            ("question", "fg:magenta bold"),
            ("answer", "fg:white"),
        ]
    )

    while True:
        try:
            # Використовуємо questionary для вводу з автодоповненням
            user_input = questionary.text(
                HELP_PROMPT,
                completer=completer,
                history=history,
                qmark="",
                style=style,
                complete_style=CompleteStyle.COLUMN,
            ).ask()

            if user_input is None:
                break

            command, args, kwargs = cli.parse_input(user_input)

            if command in ["close", "exit"]:
                logger.info("Application exit requested")
                storage_info = get_storage_info()
                print("\n[dim]Дані збережено у:[/dim]")
                print(f"[dim]📁 {storage_info['addressbook']}[/dim]")
                print(f"[dim]📓 {storage_info['notes']}[/dim]\n")
                print(EXIT_MSG)
                break

            if command in commands:
                logger.info(f"Executing command: {command}")
                commands[command](args, kwargs)
            else:
                logger.warning(f"Unknown command attempted: {command}")
                print(UNKNOWN_COMMAND)
        except KeyboardInterrupt:
            logger.info("Application exit via KeyboardInterrupt")
            print(EXIT_MSG)
            break
        except Exception as e:
            logger.error(
                f"Unexpected error in main loop: {str(e)}", exc_info=True
            )
            print(f"[bold red]Помилка:[/bold red] {e}")
            break


if __name__ == "__main__":
    main()
