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
from contacts.decorators import input_error
from contacts.record import Record
from notes.notebook import Notebook



@input_error
def add_contact(args: list[str], book: AddressBook, **kwargs) -> str:
    """
    Додає новий контакт або оновлює існуючий.
    Приймає ім'я, один або декілька телефонів, email та адресу.
    Ім'я є обов'язковим.
    """
    if not args:
        return "Введіть ім'я контакту."

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

    # if email:
    #     record.add_email(email)
    
    if address:
        record.edit_address(address)
    
    if birthday: 
        record.edit_birthday(birthday)
        
    return f"{message} Новий запис:\n{record}"


@input_error
def edit_phone(args: list[str], book: AddressBook, **kwargs) -> str:
    """
    Змінює телефон контакту.
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
    Змінює email контакту.
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
    Редагує день народження контакту.
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
    Редагує адресу контакту.
    """
    name, address = args
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
    Видаляє контакт за ім'ям.
    """
    name = args[0]
    book.delete(name)
    return f"Контакт {name} видалено."

@input_error
def add_note(args: list[str], notebook: Notebook, **kwargs) -> str:
    """
    Додає нотатку.
    Формат (через main.py + parse_input):
      add_note "text of note" [tag1 tag2 ...]
    """
    if not args:
        return ' Введіть текст нотатки. Формат: add_note "text" [tag1 tag2...]'

    text = args[0]
    tags = args[1:] if len(args) > 1 else []

    note = notebook.add_note(text, tags)
    tags_str = ", ".join(tags) if tags else "немає"
    return f"📝 Нотатку #{note.id} додано. Теги: {tags_str}"


@input_error
def do_add_note(self, line):
        """add-note "text of note" [tag1 tag2 ...] — додає нотатку з текстом і необов'язковими тегами"""
        
        if not line:
            print('Введіть текст нотатки. Формат: add-note "text" [tag1 tag2...]')
            return
        # очікуємо формат: "текст нотатки" теги...
        if '"' not in line:
            print('Обгорніть текст у лапки: add-note "text" tag1 tag2')
            return
        first_quote = line.find('"')
        last_quote = line.rfind('"')
        text = line[first_quote + 1:last_quote]
        tags_part = line[last_quote + 1:].strip()
        tags = tags_part.split() if tags_part else []
        
        note = self.notebook.add_note(text, tags)
        save_notes(self.notebook)
        print(f"📝 Нотатку #{note.id} додано. Теги: {', '.join(tags) if tags else 'немає'}")
    
def do_search_notes(self, line):
        """search-notes <query> — пошук по тексту і тегах"""
        if not line:
            print("Usage: search-notes <query> - пошук по тексту і тегах")
            return
        results = self.notebook.find(line)
        if not results:
            print("📭 Нотатки не знайдено")
            return
        
        table = PrettyTable(["ID", "Текст", "Теги"])
        for n in results:
            table.add_row([n.id, n.text[:40] + ("..." if len(n.text) > 40 else ""), ", ".join(n.tags)])
        print(table)
    
def do_notes_by_tag(self, line):
        """notes-by-tag <tag> — нотатки за тегом"""
        if not line:
            print("Usage: notes-by-tag <tag> - показує нотатки з вказаним тегом")
            return
        results = self.notebook.find_by_tag(line)
        if not results:
            print("Нотатки з таким тегом не знайдено")
            return
        table = PrettyTable(["ID", "Текст", "Теги"])
        for n in results:
            table.add_row([n.id, n.text[:40] + ("..." if len(n.text) > 40 else ""), ", ".join(n.tags)])
        print(table)
    
def do_delete_note(self, line):
        """delete-note <id> — видалити нотатку за ID"""
        if not line.isdigit():
            print("Usage: delete-note <id> - видаляє нотатку за її ID")
            return
        note_id = int(line)
        if self.notebook.delete_note(note_id):
            save_notes(self.notebook)
            print(f"🗑️ Нотатку #{note_id} видалено")
        else:
            print("Нотатку не знайдено")
