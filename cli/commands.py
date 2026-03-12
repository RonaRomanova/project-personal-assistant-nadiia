"""Обробники команд для CLI інтерфейсу.

Цей модуль містить функції обробники команд, які обробляють введення користувача
та взаємодіють з адресною книгою.

Функції:
    add_contact: Додає новий контакт або телефон до існуючого контакту.
    change_contact: Змінює телефон контакту.
    show_phone: Показує всі телефони контакту.
    show_all: Показує всі контакти адресної книги.
    add_birthday: Додає день народження контакту.
    show_birthday: Показує день народження контакту.
    birthdays: Показує список найближчих днів народження.
"""
from contacts import AddressBook
from contacts.decorators import input_error
from contacts.record import Record


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
        record.add_address(address)
    
    if birthday: 
        record.add_birthday(birthday)
        
    return message


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
    return "Контакт оновлено."


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
    return "Контакт оновлено."


@input_error
def edit_contact(args: list[str], book: AddressBook, **kwargs) -> str:
    """
    Редагує день народження або адресу контакту.
    """
    name = args[0]
    record = book.find(name)

    if record is None:
        raise KeyError

    if "birthday" in kwargs:
        record.add_birthday(kwargs["birthday"])
    
    if "address" in kwargs:
        record.add_address(kwargs["address"])

    return "Контакт оновлено."


@input_error
def show_phone(args: list[str], book: AddressBook, **kwargs) -> str:
    """
    Показує всі телефони контакту.
    """
    name = args[0]
    record = book.find(name)

    if record is None:
        raise KeyError

    return "; ".join(phone.value for phone in record.phones)


@input_error
def show_all(book: AddressBook, **kwargs) -> str:
    """
    Показує всі контакти адресної книги.
    """
    if not book.data:
        return "Контактів не збережено."

    return "\n".join(str(record) for record in book.data.values())


@input_error
def add_birthday(args: list[str], book: AddressBook, **kwargs) -> str:
    """
    Додає день народження контакту.
    """
    name, birthday = args
    record = book.find(name)

    if record is None:
        raise KeyError

    record.add_birthday(birthday)
    return "День народження додано."


@input_error
def show_birthday(args: list[str], book: AddressBook, **kwargs) -> str:
    """
    Показує день народження контакту.
    """
    name = args[0]
    record = book.find(name)

    if record is None:
        raise KeyError

    if record.birthday is None:
        return "День народження не встановлено."

    return record.birthday.value


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
