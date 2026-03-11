from contacts import input_error, Record, AddressBook


@input_error
def add_contact(args: list[str], book: AddressBook) -> str:
    """
    Додає новий контакт або телефон до існуючого контакту.
    """
    name, phone, *_ = args
    record = book.find(name)

    message = "Контакт оновлено."

    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Контакт додано."

    record.add_phone(phone)
    return message


@input_error
def change_contact(args: list[str], book: AddressBook) -> str:
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
def show_phone(args: list[str], book: AddressBook) -> str:
    """
    Показує всі телефони контакту.
    """
    name = args[0]
    record = book.find(name)

    if record is None:
        raise KeyError

    return "; ".join(phone.value for phone in record.phones)


@input_error
def show_all(book: AddressBook) -> str:
    """
    Показує всі контакти адресної книги.
    """
    if not book.data:
        return "Контактів не збережено."

    return "\n".join(str(record) for record in book.data.values())


@input_error
def add_birthday(args: list[str], book: AddressBook) -> str:
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
def show_birthday(args: list[str], book: AddressBook) -> str:
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
def birthdays(args: list[str], book: AddressBook) -> str:
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
