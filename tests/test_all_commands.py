"""
Комплексні тести для всіх команд CLI.

Цей модуль тестує всю функціональність команд, включаючи роботу з контактами,
телефонами та днями народження.
"""

import unittest
import tempfile
import os
from contacts import AddressBook, Record
from cli import (
    add_contact,
    change_contact,
    show_phone,
    show_all,
    add_birthday,
    show_birthday,
    birthdays,
)
from storage import save_data, load_data


class TestAddContactCommand(unittest.TestCase):
    """Тести для команди додавання контакту."""

    def setUp(self):
        """Підготовка до кожного тесту."""
        self.book = AddressBook()

    def test_add_new_contact(self):
        """Тест додавання нового контакту."""
        result = add_contact(["Alice", "+380988786777"], self.book)
        self.assertEqual(result, "Контакт додано.")
        self.assertIsNotNone(self.book.find("Alice"))

    def test_add_phone_to_existing_contact(self):
        """Тест додавання телефону до існуючого контакту."""
        add_contact(["Bob", "+380988786777"], self.book)
        result = add_contact(["Bob", "+380965544321"], self.book)
        self.assertEqual(result, "Контакт оновлено.")
        
        record = self.book.find("Bob")
        self.assertEqual(len(record.phones), 2)

    def test_add_duplicate_phone(self):
        """Тест додавання дублікатного телефону."""
        add_contact(["Charlie", "+380988786777"], self.book)
        result = add_contact(["Charlie", "+380988786777"], self.book)
        
        record = self.book.find("Charlie")
        self.assertEqual(len(record.phones), 1, "Дублікати повинні видаляться")

    def test_add_contact_invalid_phone(self):
        """Тест додавання контакту з невалідним номером."""
        result = add_contact(["Diana", "123"], self.book)
        # Помилка повинна бути про кількість цифр
        self.assertIn("цифр", result.lower())


class TestChangeContactCommand(unittest.TestCase):
    """Тести для команди зміни контакту."""

    def setUp(self):
        """Підготовка до кожного тесту."""
        self.book = AddressBook()
        add_contact(["Eve", "+380988786777"], self.book)

    def test_change_phone(self):
        """Тест зміни телефону."""
        result = change_contact(["Eve", "+380988786777", "+380965544321"], self.book)
        self.assertEqual(result, "Контакт оновлено.")
        
        record = self.book.find("Eve")
        phones = [p.value for p in record.phones]
        self.assertIn("+380965544321", phones)
        self.assertNotIn("+380988786777", phones)

    def test_change_nonexistent_contact(self):
        """Тест зміни неіснуючого контакту."""
        result = change_contact(["Unknown", "+380988786777", "+380965544321"], self.book)
        self.assertEqual(result, "Контакт не знайдено.")


class TestShowPhoneCommand(unittest.TestCase):
    """Тести для команди показання телефону."""

    def setUp(self):
        """Підготовка до кожного тесту."""
        self.book = AddressBook()

    def test_show_phone_single(self):
        """Тест показання одного телефону."""
        add_contact(["Frank", "+380988786777"], self.book)
        result = show_phone(["Frank"], self.book)
        self.assertEqual(result, "+380988786777")

    def test_show_phone_multiple(self):
        """Тест показання кількох телефонів."""
        add_contact(["Grace", "+380988786777"], self.book)
        add_contact(["Grace", "+380965544321"], self.book)
        result = show_phone(["Grace"], self.book)
        
        self.assertIn("+380988786777", result)
        self.assertIn("+380965544321", result)

    def test_show_phone_nonexistent(self):
        """Тест показання телефону неіснуючого контакту."""
        result = show_phone(["Unknown"], self.book)
        self.assertEqual(result, "Контакт не знайдено.")


class TestShowAllCommand(unittest.TestCase):
    """Тести для команди показання всіх контактів."""

    def setUp(self):
        """Підготовка до кожного тесту."""
        self.book = AddressBook()

    def test_show_all_empty(self):
        """Тест показання порожної книги."""
        result = show_all(self.book)
        self.assertEqual(result, "Контактів не збережено.")

    def test_show_all_multiple_contacts(self):
        """Тест показання кількох контактів."""
        add_contact(["Henry", "+380988786777"], self.book)
        add_contact(["Irene", "+380965544321"], self.book)
        
        result = show_all(self.book)
        self.assertIn("Henry", result)
        self.assertIn("Irene", result)


class TestBirthdayCommands(unittest.TestCase):
    """Тести для команд днів народження."""

    def setUp(self):
        """Підготовка до кожного тесту."""
        self.book = AddressBook()

    def test_add_birthday(self):
        """Тест додавання дня народження."""
        add_contact(["Jack", "+380988786777"], self.book)
        result = add_birthday(["Jack", "15.03.1990"], self.book)
        
        self.assertEqual(result, "День народження додано.")
        record = self.book.find("Jack")
        self.assertEqual(record.birthday.value, "15.03.1990")

    def test_show_birthday(self):
        """Тест показання дня народження."""
        add_contact(["Kate", "+380988786777"], self.book)
        add_birthday(["Kate", "20.05.1985"], self.book)
        
        result = show_birthday(["Kate"], self.book)
        self.assertEqual(result, "20.05.1985")

    def test_show_birthday_not_set(self):
        """Тест показання дня народження, коли його нема."""
        add_contact(["Leo", "+380988786777"], self.book)
        result = show_birthday(["Leo"], self.book)
        self.assertEqual(result, "День народження не встановлено.")

    def test_add_invalid_birthday(self):
        """Тест додавання невалідної дати."""
        add_contact(["Mia", "+380988786777"], self.book)
        result = add_birthday(["Mia", "15/03/1990"], self.book)
        self.assertIn("формат", result.lower())

    def test_birthdays_command(self):
        """Тест команди найближчих днів народження."""
        add_contact(["Noah", "+380988786777"], self.book)
        result = birthdays([], self.book)
        
        # Повинна бути строка, не помилка
        self.assertIsInstance(result, str)


class TestStorageIntegration(unittest.TestCase):
    """Інтеграційні тести для зберігання та завантаження."""

    def setUp(self):
        """Підготовка до кожного тесту."""
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pkl")
        self.temp_filename = self.temp_file.name
        self.temp_file.close()

    def tearDown(self):
        """Очищення після тесту."""
        if os.path.exists(self.temp_filename):
            os.remove(self.temp_filename)

    def test_save_and_load_with_duplicate_phones(self):
        """Тест збереження та завантаження контактів з дублікатними номерами."""
        book = AddressBook()
        add_contact(["Oliver", "+380988786777"], book)
        add_contact(["Oliver", "+380988786777"], book)
        add_contact(["Oliver", "+380965544321"], book)
        
        save_data(book, self.temp_filename)
        loaded_book = load_data(self.temp_filename)
        
        oliver = loaded_book.find("Oliver")
        self.assertEqual(len(oliver.phones), 2)

    def test_save_and_load_complete_contact(self):
        """Тест збереження та завантаження контакту з всією інформацією."""
        book = AddressBook()
        add_contact(["Patricia", "+380988786777"], book)
        add_contact(["Patricia", "+380965544321"], book)
        add_birthday(["Patricia", "10.12.1992"], book)
        
        save_data(book, self.temp_filename)
        loaded_book = load_data(self.temp_filename)
        
        patricia = loaded_book.find("Patricia")
        self.assertEqual(len(patricia.phones), 2)
        self.assertEqual(patricia.birthday.value, "10.12.1992")


class TestFieldValidation(unittest.TestCase):
    """Тести для валідації полів."""

    def test_phone_format_10_digits(self):
        """Тест формату телефону з 10 цифрами (має починатися з 0)."""
        result = add_contact(["Quinn", "0971234567"], AddressBook())
        self.assertEqual(result, "Контакт додано.")

    def test_phone_format_with_plus(self):
        """Тест формату телефону з +."""
        result = add_contact(["Rachel", "+380988786777"], AddressBook())
        self.assertEqual(result, "Контакт додано.")

    def test_phone_too_short(self):
        """Тест надто короткого номера."""
        result = add_contact(["Sam", "123"], AddressBook())
        # Помилка повинна містити інформацію про цифри
        self.assertIn("цифр", result.lower())

    def test_birthday_valid_format(self):
        """Тест валідного формату дати."""
        book = AddressBook()
        add_contact(["Tina", "+380988786777"], book)
        result = add_birthday(["Tina", "01.01.2000"], book)
        self.assertEqual(result, "День народження додано.")

    def test_birthday_invalid_format(self):
        """Тест невалідного формату дати."""
        book = AddressBook()
        add_contact(["Uma", "+380988786777"], book)
        result = add_birthday(["Uma", "2000-01-01"], book)
        self.assertIn("формат", result.lower())


if __name__ == "__main__":
    unittest.main()
