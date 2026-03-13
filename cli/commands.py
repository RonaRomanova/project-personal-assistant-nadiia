"""Обробники команд для CLI інтерфейсу.

Цей модуль містить функції обробники команд, які обробляють введення користувача
та взаємодіють з адресною книгою.

Функції:
    add_contact: Додає новий контакт або телефон до існуючого контакту.
    change_contact: Змінює телефон контакту.
    show_phone: Показує всі телефони контакту.
    show_all: Показує всі контакти адресної книги.
    add_birthday: Додає день народження контакту.
    birthdays: Показує список найближчих днів народження.
"""
import email
import shlex

from contacts import AddressBook
from cli.validators import input_error
from contacts.record import Record
from notes.notebook import Notebook
from prettytable import PrettyTable
from typing import Optional

from storage.file_storage import save_notes




@input_error
def add_contact(args: list[str], book: AddressBook, **kwargs) -> str:
    """
    Додає новий контакт або оновлює існуючий. Приймає ім'я, один або декілька телефонів, email та адресу.
    Ім'я є обов'язковим. Формат: add <Ім'я> [телефон1] [телефон2] ... [email=email] [address=адреса] [birthday=дата]
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
    for email in (emails or []):
        record.add_email(email)
    
    if address:
        record.edit_address(address)
    
    if birthday: 
        record.edit_birthday(birthday)
        
    return f"{message} Новий запис:\n{record}"


@input_error
def edit_phone(args: list[str], book: AddressBook, **kwargs) -> str:
    """
    Змінює телефон контакту. Формат: edit-phone <Ім'я> <старий_телефон> <новий_телефон>
    """
    name, old_phone, new_phone = args
    record = book.find(name)

    if record is None:
        raise KeyError

    record.edit_phone(old_phone, new_phone)
    return f"Контакт оновлено. Новий запис:\n{record}"


@input_error
def edit_email(args: list[str], book: AddressBook, **kwargs) -> str:
    """
    Змінює email контакту. Формат: edit-email <Ім'я> <старий_email> <новий_email>
    """
    name, old_email, new_email = args
    record = book.find(name)

    if record is None:
        raise KeyError

    record.edit_email(old_email, new_email)
    return f"Контакт оновлено. Новий запис:\n{record}"


@input_error
def show_all(book: AddressBook, **kwargs) -> str:
    """
    Показує всі контакти адресної книги.
    """
    if not book.data:
        return f"Контактів не збережено. Використайте команду 'add' для додавання першого контакту."

    return "\n".join(str(record) for record in book.data.values())


@input_error
def edit_birthday(args: list[str], book: AddressBook, **kwargs) -> str:
    """
    Редагує день народження контакту. Формат: edit-birthday <Ім'я> <ДД.ММ.РРРР>
    """
    name, birthday = args
    record = book.find(name)

    if record is None:
        raise KeyError

    record.edit_birthday(birthday)
    return f"День народження оновлено. Новий запис:\n{record}"

@input_error
def edit_address(args: list[str], book: AddressBook, **kwargs) -> str:
    """
    Редагує адресу контакту. Формат: edit-address <Ім'я> <Нова адреса>
    """
    name, *address_parts = args
    if not address_parts: # Адреса має бути введена
        raise IndexError
    address = " ".join(address_parts)
    record = book.find(name)

    if record is None:
        raise KeyError

    record.edit_address(address)
    return f"Адресу оновлено. Новий запис:\n{record}"


@input_error
def birthdays(args: list[str], book: AddressBook, **kwargs) -> str:
    """
    Показує список найближчих днів народження.
    """
    upcoming_birthdays = book.get_upcoming_birthdays()

    if not upcoming_birthdays:
        return "Немає днів народження на наступний тиждень."

    return "\n".join(
        f"{item['name']}: {item['congratulation_date']}"
        for item in upcoming_birthdays
    )

@input_error
def find_contact(args: list[str], book: AddressBook) -> str:
    """
    Знаходить контакт за ім'ям, телефоном або адресою. Показує всі дані контакту.
    """
    arguments = {}  
    for arg in args:
        if "=" in arg:
            key, value = arg.split("=", 1)
            arguments[key] = value
        else:
            arguments["name"] = arg

    result = set()
    
    name = arguments.get("name") or args[0] if args else None
    result.add(book.find(name))
    
    phone = arguments.get("phone")
    if phone:
        for record in book.data.values():
            if any(p.value == phone for p in record.phones):
                result.add(record)
    
    email = arguments.get("email")
    result.add(book.find(email))
    if email:
        for record in book.data.values():
            if any(e.value == email for e in record.emails):
                result.add(record)

    address = arguments.get("address")
    if address:
        for record in book.data.values():
            if record.address and record.address.value.lower() == address.lower():
                result.add(record)

    if None in result:
        result.remove(None)

    if not result:
        return f"Контакт не знайдено. Спробуйте інші параметри пошуку. Формат: find 'Elon Musk' phone=+380991234999 email=asd@example.com address='Mars'"

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
    """
    Додає нотатку. Формат: add-note <"текст нотатки"> [тег1] [тег2] ...
    """
    text = args[0]
    tags = args[1:] if len(args) > 1 else []

    note = notebook.add_note(text, tags)
    tags_str = ", ".join(tags) if tags else "немає"
    return f"📝 Нотатку #{note.id} {note.text} додано. Теги: {tags_str}"

@input_error
def edit_note(args: list[str], notebook: Notebook, **kwargs) -> str:
    """
    Редагує текст нотатки. Формат: edit-note <ID> <"новий текст">
    """
    try:
        note_id = int(args[0])
    except ValueError:
        return "ID має бути числом."

    new_text = args[1]
    
    if notebook.edit_note(note_id, new_text):
        return f"Нотатку #{note_id} {new_text} оновлено."
    else:
        return "Нотатку не знайдено."
    
@input_error
def edit_tag(args: list[str], notebook: Notebook, **kwargs) -> str:
    """
    Редагує ТЕГИ. Формат: edit-tag <ID> <add|delete> <тег1> [тег2...]
    """
    try:
        note_id = int(args[0])
        action = args[1].lower()
        tags_input = args[2:]
    except ValueError:
        return "ID має бути числом."
    
    note = notebook._notes.get(note_id)
    if not note:
        return f"Нотатку #{note_id} не знайдено."
    
    match action:
        case "add":
            added = []
            for tag in tags_input:
                if note.add_tag(tag):
                    added.append(tag)
            return f"Додано: {', '.join(added)} → #{note_id} {note.text} [Теги: {', '.join(note.tags)}]"
        
        case "delete":
            if len(tags_input) != 1:
                return "Для видалення тегу вкажіть лише один тег. Формат: edit-tag <ID> delete <tag>"
            if note.delete_tag(tags_input[0]):
                return f"Видалено '{tags_input[0]}' з #{note_id} {note.text} [Теги: {', '.join(note.tags)}]"
            return f"Тег '{tags_input[0]}' не знайдено."
        
        case _:
            return f"Дія '{action}': add/delete."
           

@input_error
def delete_note(args: list[str], notebook: Notebook, **kwargs) -> str:
    """
    Видаляє нотатку за ID. Формат: delete-note <ID>
    """
    try:
        note_id = int(args[0])
    except ValueError:
        return "ID має бути числом."

    if notebook.delete_note(note_id):
        return f"Нотатку #{note_id} видалено."
    else:
        return "Нотатку не знайдено."

@input_error
def find_note(args: list[str], notebook: Notebook, **kwargs) -> str:
    """
    Шукає нотатки за текстом або тегами. Формат: find-note <пошуковий_запит>
    """
    query = args[0] 
    matches = notebook.find(query)
    
    if not matches:
        return "Нотатки не знайдено."
    
    return "\n".join(f"#{n.id}: {n.text} [Теги: {', '.join(n.tags)}]" for n in matches)


@input_error
def all_notes(notebook: Notebook, **kwargs) -> str:
    """
    Показує всі нотатки у вигляді таблиці. Формат: id | name | tags (#tag1, #tag2)
    """
    notes = notebook.all_notes()
    if not notes:
        return "📝 Нотаток немає."
    
    # Створюємо таблицю
    table = PrettyTable()
    table.field_names = ["ID", "Notes", "Tags"]
    table.align["Notes"] = "l"      # ліве вирівнювання для тексту
    table.align["Tags"] = "l"
    
    for n in notes:
        # Теги з # + комами
        tags_str = ", ".join(f"#{tag}" for tag in n.tags) if n.tags else "немає"
        # Обрізаємо довгий текст
        name_short = (n.text[:50] + "..." if len(n.text) > 50 else n.text)
        
        table.add_row([n.id, name_short, tags_str])
    
    return str(table)
