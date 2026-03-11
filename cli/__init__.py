"""
Модуль CLI для операцій командного рядка.

Цей модуль надає утиліти для розбору та валідації вводу користувача,
а також обробники команд для помічника бота.

Функції:
    parse_input: Розбирає рядок введення користувача на команду та аргументи.
    add_contact: Додає новий контакт або телефон до існуючого контакту.
    change_contact: Змінює телефон контакту.
    show_phone: Показує всі телефони контакту.
    show_all: Показує всі контакти адресної книги.
    add_birthday: Додає день народження контакту.
    show_birthday: Показує день народження контакту.
    birthdays: Показує список найближчих днів народження.

Приклад:
    >>> from cli import parse_input, add_contact
    >>> cmd, args = parse_input("add John 1234567890")
    >>> print(cmd, args)
    add ['John', '1234567890']
"""

from .validators import parse_input
from .commands import (
    add_contact,
    change_contact,
    show_phone,
    show_all,
    add_birthday,
    show_birthday,
    birthdays,
)

__all__ = [
    "parse_input",
    "add_contact",
    "change_contact",
    "show_phone",
    "show_all",
    "add_birthday",
    "show_birthday",
    "birthdays",
]
