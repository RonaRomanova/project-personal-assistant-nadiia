"""
Модуль контактів для керування записами адресної книги та інформацією про контакти.

Цей модуль надає класи для керування контактами з наступними компонентами:

Класи:
    AddressBook: Керує колекцією записів контактів з операціями пошуку, додавання та видалення.
    Record: Представляє один контакт з інформацією про ім'я, телефони та день народження.
    Field: Базовий клас для полів контакту.
    Name: Клас поля для зберігання імен контактів.
    Phone: Клас поля для зберігання номерів телефонів (10 цифр).
    Birthday: Клас поля для зберігання днів народження у форматі DD.MM.YYYY.

Приклад:
    >>> from contacts import AddressBook, Record
    >>> book = AddressBook()
    >>> record = Record("John Doe")
    >>> record.add_phone("1234567890")
    >>> book.add_record(record)
"""

from .address_book import AddressBook
from .fields import Field, Name, Phone, Birthday, Email, Address
from .record import Record
from .decorators import input_error

__all__ = [
    "AddressBook",
    "Field",
    "Name",
    "Phone",
    "Email",
    "Address",
    "Birthday",
    "Record",
    "input_error"
]

