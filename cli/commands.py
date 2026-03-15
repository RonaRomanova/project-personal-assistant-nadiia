from datetime import datetime

from rich.table import Table
from rich import box

from cli.validators import input_error
from contacts import AddressBook
from contacts.record import Record
from notes.notebook import Notebook
from contacts.constants import (
    UKRAINIAN_DATE_FORMAT,
    NOT_SPECIFIED,
    NO_NOTES,
    CONTACT_NOT_FOUND,
    NOTE_NOT_FOUND,
    TABLE_NAME_MAX_WIDTH,
    TABLE_PHONE_MAX_WIDTH,
    TABLE_EMAIL_MAX_WIDTH,
    TABLE_ADDRESS_MAX_WIDTH,
    TABLE_NOTE_MAX_WIDTH,
    TABLE_UPCOMING_NAME_MAX_WIDTH,
)


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

    return f"{message} Новий запис:\n{record}"


@input_error
def edit_phone(args: list[str], book: AddressBook, **kwargs) -> str:
    """Змінює телефон контакту."""
    name, old_phone, new_phone = args
    record = book.find(name)
    if record is None:
        return CONTACT_NOT_FOUND
    record.edit_phone(old_phone, new_phone)
    return f"Контакт оновлено. Новий запис:\n{record}"


@input_error
def edit_email(args: list[str], book: AddressBook, **kwargs) -> str:
    """Змінює email контакту."""
    name, old_email, new_email = args
    record = book.find(name)
    if record is None:
        return CONTACT_NOT_FOUND
    record.edit_email(old_email, new_email)
    return f"Контакт оновлено. Новий запис:\n{record}"


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
    table.add_column("Phone", style="magenta", header_style="bold magenta")
    table.add_column("Email", style="yellow", header_style="bold yellow")
    table.add_column("Birthday", justify="center", style="green", header_style="bold green")
    table.add_column("Address", style="blue", header_style="bold blue")

    for record in book.data.values():
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
    return f"День народження оновлено. Новий запис:\n{record}"


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
    return f"Адресу оновлено. Новий запис:\n{record}"


@input_error
def birthdays(args: list[str], book: AddressBook, **kwargs) -> str:
    """Показує найближчі дні народження у вигляді таблиці."""
    upcoming = book.get_upcoming_birthdays()
    if not upcoming:
        return "Немає днів народження на наступний тиждень."

    table = Table(title="Upcoming Birthdays", box=box.ROUNDED)
    table.add_column("Name", style="cyan", header_style="bold cyan")
    table.add_column("Birthday", justify="center", style="green", header_style="bold green")
    table.add_column("Days Left", justify="right", style="magenta", header_style="bold magenta")

    today = datetime.now().date()

    for item in upcoming:
        name = item["name"]
        date_str = item["congratulation_date"]
        date_obj = datetime.strptime(date_str, UKRAINIAN_DATE_FORMAT).date()
        days_left = str((date_obj - today).days)

        table.add_row(name, date_str, days_left)

    return table


@input_error
def find_contact(args: list[str], book: AddressBook) -> str:
    """Знаходить контакт за ім'ям, телефоном або адресою."""
    arguments = {}
    for arg in args:
        if "=" in arg:
            key, value = arg.split("=", 1)
            arguments[key] = value
        else:
            arguments["name"] = arg

    result = set()
    name = arguments.get("name") or (args[0] if args else None)
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
            if any(email.lower() in e.value.lower() for e in record.emails):
                result.add(record)

    address = arguments.get("address")
    if address:
        for record in book.data.values():
            if record.address and address.lower() in record.address.value.lower():
                result.add(record)

    if None in result:
        result.remove(None)

    if not result:
        return CONTACT_NOT_FOUND

    return "\n".join(str(record) for record in result)


@input_error
def delete_contact(args: list[str], book: AddressBook) -> str:
    """
    Видаляє контакт за ім'ям. Формат: delete <Ім'я>
    """
    name = args[0]
    book.delete(name)
    return f"Контакт {name} видалено."


@input_error
def add_note(args: list[str], notebook: Notebook, **kwargs) -> str:
    """Додає нотатку."""
    text = args[0]
    tags = args[1:] if len(args) > 1 else []
    note = notebook.add_note(text, tags)
    tags_str = ", ".join(tags) if tags else NOT_SPECIFIED
    return f"📝 Нотатку #{note.id} {note.text} додано. Теги: {tags_str}"


@input_error
def edit_note(args: list[str], notebook: Notebook, **kwargs) -> str:
    """Редагує текст нотатки."""
    try:
        note_id = int(args[0])
    except (ValueError, IndexError):
        return "ID має бути числом."
    new_text = args[1]
    if notebook.edit_note(note_id, new_text):
        return f"Нотатку #{note_id} {new_text} оновлено."
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
        added = [t for t in tags_input if note.add_tag(t)]
        return (f"Додано: {', '.join(added)} → #{note_id} "
                f"{note.text} [Теги: {', '.join(note.tags)}]")
    elif action == "delete":
        if len(tags_input) != 1:
            return "Вкажіть лише один тег для видалення."
        if note.delete_tag(tags_input[0]):
            return (f"Видалено '{tags_input[0]}' з #{note_id} "
                    f"{note.text} [Теги: {', '.join(note.tags)}]")
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
        return f"Нотатку #{note_id} видалено."
    return NOTE_NOT_FOUND


@input_error
def find_note(args: list[str], notebook: Notebook, **kwargs) -> str:
    """Шукає нотатки за текстом або тегами."""
    query = args[0]
    matches = notebook.find(query)
    if not matches:
        return NOTE_NOT_FOUND
    return "\n".join(f"#{n.id}: {n.text} [Теги: {', '.join(n.tags)}]"
                     for n in matches)


@input_error
def all_notes(notebook: Notebook, **kwargs) -> str:
    """Показує всі нотатки у вигляді таблиці."""
    notes = notebook.all_notes()
    if not notes:
        return NO_NOTES

    table = Table(title="Notebook", box=box.ROUNDED)
    table.add_column("ID", justify="right", style="cyan", header_style="bold cyan")
    table.add_column("Notes", style="white", header_style="bold white")
    table.add_column("Tags", style="magenta", header_style="bold magenta")

    for n in notes:
        tags_str = (", ".join(f"#{tag}" for tag in n.tags)
                    if n.tags else NOT_SPECIFIED)
        table.add_row(str(n.id), n.text, tags_str)
    return table
