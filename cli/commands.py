from datetime import datetime
from typing import List

from rich import box
from rich.table import Table

from cli.validators import input_error
from contacts import AddressBook
from contacts.constants import (
    CONTACT_NOT_FOUND,
    DATE_FORMAT,
    NO_NOTES,
    NOT_SPECIFIED,
    NOTE_NOT_FOUND,
    UKRAINIAN_DATE_FORMAT,
)
from contacts.record import Record
from notes.note import Note
from notes.notebook import Notebook
from utils import get_logger, parse_date

logger = get_logger()


def render_record(record: Record, title: str = None) -> Table:
    """Створює Rich Table для відображення одного або декількох контактів."""
    table = Table(title=title, box=box.ROUNDED)
    table.add_column("Name", style="cyan", header_style="bold cyan")
    table.add_column(
        "Phone", style="dark_orange3", header_style="bold dark_orange3"
    )
    table.add_column("Email", style="yellow", header_style="bold yellow")
    table.add_column(
        "Birthday", justify="center", style="green", header_style="bold green"
    )
    table.add_column("Address", style="blue", header_style="bold blue")

    name = record.name.value
    phone = ", ".join(p.value for p in record.phones) or "-"
    email = ", ".join(e.value for e in record.emails) or "-"
    birthday = record.birthday.value if record.birthday else "-"
    address = record.address.value if record.address else "-"

    table.add_row(name, phone, email, birthday, address)
    return table


def render_notes(notes: List[Note], title: str = None) -> Table:
    """Створює Rich Table для відображення нотаток."""
    if not notes:
        return title or "Нотаток не знайдено."

    table = Table(title=title, box=box.ROUNDED)
    table.add_column(
        "ID", justify="right", style="cyan", header_style="bold cyan"
    )
    table.add_column("Notes", style="green", header_style="bold green")
    table.add_column(
        "Tags", style="dark_orange3", header_style="bold dark_orange3"
    )

    for n in notes:
        tags_str = (
            ", ".join(f"#{tag}" for tag in n.tags) if n.tags else NOT_SPECIFIED
        )
        table.add_row(str(n.id), n.text, tags_str)
    return table


@input_error
def add_contact(args: list[str], book: AddressBook, **kwargs) -> str:
    """
    Додає новий контакт або оновлює існуючий.
    Формат: add <Ім'я> [телефон1] [телефон2] ... [email=email] [address=ad]
    """
    name = args[0]
    phones = args[1:]

    emails = kwargs.get("email")
    address = kwargs.get("address")
    birthday = kwargs.get("birthday")

    record = book.find(name)
    message = "Контакт оновлено."

    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Контакт додано."

    for phone in phones:
        record.add_phone(phone)

    if isinstance(emails, str):
        emails = [emails]
    for email in emails or []:
        record.add_email(email)

    if address:
        record.edit_address(address)
    if birthday:
        record.edit_birthday(birthday)

    logger.info(
        f"Command add-contact executed for '{name}'. Result: {message}"
    )
    return render_record(record, title=message)


@input_error
def edit_phone(args: list[str], book: AddressBook, **kwargs) -> str:
    """Змінює телефон контакту."""
    name, old_phone, new_phone = args
    record = book.find(name)
    if record is None:
        return CONTACT_NOT_FOUND
    record.edit_phone(old_phone, new_phone)
    logger.info(f"Phone edited for '{name}': {old_phone} -> {new_phone}")
    return render_record(record, title="Контакт оновлено.")


@input_error
def edit_email(args: list[str], book: AddressBook, **kwargs) -> str:
    """Змінює email контакту."""
    name, old_email, new_email = args
    record = book.find(name)
    if record is None:
        return CONTACT_NOT_FOUND
    record.edit_email(old_email, new_email)
    return render_record(record, title="Контакт оновлено.")


@input_error
def show_all(book: AddressBook, **kwargs) -> str:
    """Показує всі контакти адресної книги у вигляді таблиці."""
    if not book.data:
        return (
            "Контактів не збережено. "
            "Використайте команду 'add' для додавання першого контакту."
        )

    table = Table(title="All Contacts", box=box.ROUNDED)
    table.add_column("Name", style="cyan", header_style="bold cyan")
    table.add_column(
        "Phone", style="dark_orange3", header_style="bold dark_orange3"
    )
    table.add_column("Email", style="yellow", header_style="bold yellow")
    table.add_column(
        "Birthday", justify="center", style="green", header_style="bold green"
    )
    table.add_column("Address", style="blue", header_style="bold blue")

    for record in sorted(
        book.data.values(), key=lambda x: x.name.value.lower()
    ):
        name = record.name.value
        phones_list = list(record.phones)
        phone = ", ".join(p.value for p in phones_list) or "-"
        emails_list = list(record.emails)
        email = ", ".join(e.value for e in emails_list) or "-"
        birthday = record.birthday.value if record.birthday else "-"
        address = record.address.value if record.address else "-"

        table.add_row(name, phone, email, birthday, address)

    return table


@input_error
def edit_birthday(args: list[str], book: AddressBook, **kwargs) -> str:
    """Редагує день народження контакту."""
    name, birthday = args
    record = book.find(name)
    if record is None:
        return CONTACT_NOT_FOUND
    record.edit_birthday(birthday)
    return render_record(record, title="День народження оновлено.")


@input_error
def edit_address(args: list[str], book: AddressBook, **kwargs) -> str:
    """Редагує адресу контакту."""
    name, *address_parts = args
    if not address_parts:
        raise IndexError
    address = " ".join(address_parts)
    record = book.find(name)
    if record is None:
        return CONTACT_NOT_FOUND
    record.edit_address(address)
    return render_record(record, title="Адресу оновлено.")


@input_error
def birthdays(args: list[str], book: AddressBook, **kwargs) -> str:
    """Показує найближчі дні народження у вигляді таблиці."""
    days = 7
    if args:
        try:
            days = int(args[0])
            if days <= 0 or days > 365:
                raise ValueError
        except ValueError:
            error_msg = "Параметр 'days' має бути числом від 1 до 365."
            logger.error(f"Validation error in birthdays command: {error_msg}")
            return error_msg

    upcoming = sorted(
        book.get_upcoming_birthdays(days), key=lambda x: x["name"].lower()
    )
    if not upcoming:
        return f"Немає днів народження на наступні {days} днів."

    table = Table(title=f"Upcoming Birthdays ({days} days)", box=box.ROUNDED)
    table.add_column("Name", style="cyan", header_style="bold cyan")
    table.add_column(
        "Birthday", justify="center", style="green", header_style="bold green"
    )
    table.add_column(
        "Age", justify="center", style="magenta", header_style="bold magenta"
    )
    table.add_column(
        "Next Birthday",
        justify="center",
        style="blue",
        header_style="bold blue",
    )
    table.add_column(
        "Days Left",
        justify="right",
        style="dark_orange3",
        header_style="bold dark_orange3",
    )

    today = datetime.now().date()

    for item in upcoming:
        name = item["name"]
        orig_bday = item["original_birthday"]
        age = str(item["age"])
        date_str = item["congratulation_date"]
        date_obj = datetime.strptime(date_str, UKRAINIAN_DATE_FORMAT).date()
        days_left = str((date_obj - today).days)

        table.add_row(name, orig_bday, age, date_str, days_left)

    return table


@input_error
def find_contact(args: list[str], book: AddressBook) -> str:
    """Знаходить контакт за ім'ям, телефоном або адресою."""
    arguments = {}
    general_query = None

    if args:
        # Провіряємо, чи є в аргументах хоча б один ключ-значення (key=value)
        has_keys = any("=" in arg for arg in args)

        if not has_keys:
            general_query = args[0]
        else:
            for arg in args:
                if "=" in arg:
                    key, value = arg.split("=", 1)
                    arguments[key] = value
                else:
                    arguments["name"] = arg

    result = set()

    if general_query:
        result.update(book.search(general_query))
    else:
        name = arguments.get("name")
        if name:
            result.update(book.search_by_name(name))

        phone = arguments.get("phone")
        if phone:
            for record in book.data.values():
                if any(phone in p.value for p in record.phones):
                    result.add(record)

        email = arguments.get("email")
        if email:
            for record in book.data.values():
                if any(
                    email.lower() in e.value.lower() for e in record.emails
                ):
                    result.add(record)

        address = arguments.get("address")
        if address:
            for record in book.data.values():
                if (
                    record.address
                    and address.lower() in record.address.value.lower()
                ):
                    result.add(record)
        birthday = arguments.get("birthday")
        if birthday:
            # Спроба нормалізувати дату та знайти точний збіг
            normalized = parse_date(birthday)
            if normalized:
                try:
                    search_date = datetime.strptime(
                        normalized, DATE_FORMAT
                    ).date()
                    for record in book.data.values():
                        if (
                            record.birthday
                            and record.birthday.date_value == search_date
                        ):
                            result.add(record)
                except ValueError:
                    pass

            # Також шукаємо як звичайний рядок
            for record in book.data.values():
                if record.birthday and birthday in record.birthday.value:
                    result.add(record)
    if None in result:
        result.remove(None)

    if not result:
        return CONTACT_NOT_FOUND

    table = Table(title="Found Contacts", box=box.ROUNDED)
    table.add_column("Name", style="cyan", header_style="bold cyan")
    table.add_column(
        "Phone", style="dark_orange3", header_style="bold dark_orange3"
    )
    table.add_column("Email", style="yellow", header_style="bold yellow")
    table.add_column(
        "Birthday", justify="center", style="green", header_style="bold green"
    )
    table.add_column("Address", style="blue", header_style="bold blue")

    for record in sorted(result, key=lambda x: x.name.value.lower()):
        name = record.name.value
        phone = ", ".join(p.value for p in record.phones) or "-"
        email = ", ".join(e.value for e in record.emails) or "-"
        birthday = record.birthday.value if record.birthday else "-"
        address = record.address.value if record.address else "-"
        table.add_row(name, phone, email, birthday, address)

    return table


@input_error
def delete_contact(args: list[str], book: AddressBook) -> str:
    """
    Видаляє контакт за ім'ям. Формат: delete <Ім'я>
    """
    name = args[0]
    book.delete(name)
    logger.info(f"Contact '{name}' deleted")
    return f"Контакт {name} видалено."


@input_error
def add_note(args: list[str], notebook: Notebook, **kwargs) -> str:
    """Додає нотатку."""
    text = args[0]
    tags = args[1:] if len(args) > 1 else []
    note = notebook.add_note(text, tags)
    logger.info(f"Note added with ID {note.id}. Tags: {tags}")
    return render_notes([note], title="📝 Нотатку додано.")


@input_error
def edit_note(args: list[str], notebook: Notebook, **kwargs) -> str:
    """Редагує текст нотатки."""
    try:
        note_id = int(args[0])
    except (ValueError, IndexError):
        return "ID має бути числом."
    new_text = args[1]
    if notebook.edit_note(note_id, new_text):
        note = notebook._notes.get(note_id)
        logger.info(f"Note #{note_id} updated.")
        return render_notes([note], title="Нотатку оновлено.")
    return NOTE_NOT_FOUND


@input_error
def edit_tag(args: list[str], notebook: Notebook, **kwargs) -> str:
    """Редагує ТЕГИ. Формат: edit-tag <ID> <add|delete> <тег1> [тег2...]"""
    try:
        note_id = int(args[0])
        action = args[1].lower()
        tags_input = args[2:]
    except (ValueError, IndexError):
        return "Неправильний формат команди."

    note = notebook._notes.get(note_id)
    if not note:
        return f"Нотатку #{note_id} не знайдено."

    if action == "add":
        for t in tags_input:
            note.add_tag(t)
        return render_notes([note], title="Теги додано.")
    elif action == "delete":
        if len(tags_input) != 1:
            return "Вкажіть лише один тег для видалення."
        if note.delete_tag(tags_input[0]):
            return render_notes([note], title="Тег видалено.")
        return f"Тег '{tags_input[0]}' не знайдено."
    return "Дія має бути 'add' або 'delete'."


@input_error
def delete_note(args: list[str], notebook: Notebook, **kwargs) -> str:
    """Видаляє нотатку за ID."""
    try:
        note_id = int(args[0])
    except (ValueError, IndexError):
        return "ID має бути числом."
    if notebook.delete_note(note_id):
        logger.info(f"Note #{note_id} deleted.")
        return f"Нотатку #{note_id} видалено."
    return NOTE_NOT_FOUND


@input_error
def find_note(args: list[str], notebook: Notebook, **kwargs) -> str:
    """
    Шукає нотатки за текстом, тегами або використовуючи ключі tag=, text=.
    """
    if not args:
        return "Вкажіть запит для пошуку."

    arguments = {}
    general_query = None

    # Провіряємо, чи є в аргументах хоча б один ключ-значення (key=value)
    has_keys = any("=" in arg for arg in args)

    if not has_keys:
        general_query = args[0]
    else:
        for arg in args:
            if "=" in arg:
                key, value = arg.split("=", 1)
                arguments[key.lower()] = value
            else:
                # Якщо є змішані аргументи, перший без '=' вважаємо текстом
                if "text" not in arguments:
                    arguments["text"] = arg

    result = []

    if general_query:
        result = notebook.find(general_query)
    else:
        tag_query = arguments.get("tag")
        text_query = arguments.get("text")

        if tag_query and text_query:
            # Об'єднуємо результати пошуку за тегами та текстом,
            # видаляючи дублікати за ID
            res_tags = notebook.search_by_tag(tag_query)
            res_text = notebook.search_by_text(text_query)

            seen_ids = set()
            result = []
            for n in res_tags + res_text:
                if n.id not in seen_ids:
                    result.append(n)
                    seen_ids.add(n.id)
        elif tag_query:
            result = notebook.search_by_tag(tag_query)
        elif text_query:
            result = notebook.search_by_text(text_query)

    if not result:
        return NOTE_NOT_FOUND

    return render_notes(result, title="Found Notes")


@input_error
def all_notes(notebook: Notebook, **kwargs) -> str:
    """Показує всі нотатки у вигляді таблиці."""
    notes = notebook.all_notes()
    if not notes:
        return NO_NOTES

    return render_notes(notes, title="Notebook")
