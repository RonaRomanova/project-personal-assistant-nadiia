import shlex
from cmd import Cmd
from collections import defaultdict

from contacts.address_book import AddressBook
from notes import Notebook
from storage.file_storage import load_book, load_notes
from utils.helpers import parse_date

from .commands import (
    add_contact,
    add_note,  # додано для нотаток
    all_notes,  # додано для нотаток
    birthdays,
    delete_contact,
    delete_note,  # додано для нотаток
    edit_address,
    edit_birthday,
    edit_email,
    edit_note,  # додано для нотаток
    edit_phone,
    edit_tag,  # додано для нотаток
    find_contact,
    find_note,  # додано для нотаток
    show_all,
)


def parse_input(user_input: str):
    """
    Парсить ввід користувача, підтримуючи множинні
    значення для ключів через кому.

    Формат: <команда> <ім'я> [key=value1, value2, ...] [key2=value ...]

    - <ім'я> обов'язкове, завжди перше після команди
      (може бути в лапках).
    - Усі інші параметри мають формат ключ=значення і
      можуть йти в будь-якому порядку.
    - Якщо значення містить кому (наприклад, для переліку
      телефонів або email), воно автоматично
      розбивається на окремі значення (пробіли навколо
      ком ігноруються).
    - Якщо ключ повторюється в команді, значення
      об'єднуються.
    - Для ключів дня народження (`birthday`, `bday`,
      `день рождения`) значення нормалізується до
      YYYY-MM-DD.

    Приклад:
      add "Іван Петров" phone=0971234567, 0671234567 \\
        email=ivan@example.com, office@example.com \\
        address="вул. Хрещатик, 1" birthday="15.03.1990"

    Повертає:
      command (str): назва команди в нижньому регістрі.
      args (list): список позиційних аргументів (завжди
        містить ім'я, інші позиційні аргументи
        ігноруються або додаються з попередженням).
      kwargs (dict): словник ключових аргументів.
        Для ключів, що мають кілька значень, значенням
        буде список.
    """
    try:
        parts = shlex.split(user_input)
    except ValueError:
        # Якщо лапки незакриті – запасний варіант
        parts = user_input.split()

    if not parts:
        return "", [], {}

    command = parts[0].lower()

    # Перший після команди – обов'язкове ім'я
    if len(parts) < 2:
        return command, [], {}

    name = parts[1]
    args = [name]

    raw_kwargs = defaultdict(list)

    # Множина ключів для дня народження (регістронезалежна)
    birthday_keys = {"birthday", "bday", "день рождения"}

    for part in parts[2:]:
        if "=" in part:
            key, value_str = part.split("=", 1)

            # Розбиваємо значення за комами, якщо вони є (крім адреси)
            if key.lower() == "address":
                values = [value_str.strip()]
            else:
                values = [v.strip() for v in value_str.split(",") if v.strip()]

            for value in values:
                # Нормалізація дати, якщо це ключ дня народження
                if key.lower() in birthday_keys:
                    normalized = parse_date(value)
                    if normalized:
                        value = normalized
                raw_kwargs[key].append(value)
        else:
            # Якщо після імені зустрічається позиційний аргумент,
            # додаємо його до args (не рекомендується)
            args.append(part)

    # Перетворюємо defaultdict у звичайний dict:
    # - якщо для ключа одне значення – залишаємо рядок
    # - якщо більше – залишаємо список
    kwargs = {}
    for key, values in raw_kwargs.items():
        if len(values) == 1:
            kwargs[key] = values[0]
        else:
            kwargs[key] = values

    return command, args, kwargs


__all__ = [
    "parse_input",
    "add_contact",
    "edit_phone",
    "edit_email",
    "show_all",
    "edit_birthday",
    "edit_address",
    "birthdays",
    "find_contact",
    "delete_contact",
    "add_note",  # додано для нотаток
    "edit_note",  # додано для нотаток
    "edit_tag",  # додано для нотаток
    "delete_note",  # додано для нотаток
    "find_note",  # додано для нотаток
    "all_notes",  # додано для нотаток
]

# Основний клас CLI, який буде використовуватися для взаємодії з користувачем


class NadiiaCLI(Cmd):
    def __init__(self):
        super().__init__()
        self.book = AddressBook()
        self.notebook = Notebook()
        load_book(self.book)  # як уже є
        load_notes(self.notebook)  # додамо нижче
