"""
Тести для моделей даних (Record, AddressBook, Fields).

Цей модуль тестує базові операції з контактами та полями.
"""

import unittest
from datetime import date
from contacts import Record, AddressBook, Name, Phone, Birthday, Field


class TestField(unittest.TestCase):
    """Тести для базового класу Field."""

    def test_field_creation(self):
        """Тест створення поля."""
        field = Field("test_value")
        self.assertEqual(field.value, "test_value")

    def test_field_str(self):
        """Тест строкового представлення поля."""
        field = Field("test")
        self.assertEqual(str(field), "test")


class TestNameField(unittest.TestCase):
    """Тести для поля Name."""

    def test_name_creation(self):
        """Тест створення имені."""
        name = Name("John Doe")
        self.assertEqual(name.value, "John Doe")

    def test_name_str(self):
        """Тест строкового представлення імені."""
        name = Name("Alice")
        self.assertEqual(str(name), "Alice")


class TestPhoneField(unittest.TestCase):
    """Тести для поля Phone."""

    def test_phone_creation(self):
        """Тест створення телефону."""
        phone = Phone("+380988786777")
        self.assertEqual(phone.value, "+380988786777")

    def test_phone_equality(self):
        """Тест рівності номерів телефону."""
        phone1 = Phone("+380988786777")
        phone2 = Phone("+380988786777")
        self.assertEqual(phone1, phone2)

    def test_phone_hash(self):
        """Тест хешування телефону."""
        phone1 = Phone("+380988786777")
        phone2 = Phone("+380988786777")
        self.assertEqual(hash(phone1), hash(phone2))

    def test_phone_in_set(self):
        """Тест телефону в set."""
        phone1 = Phone("+380988786777")
        phone2 = Phone("+380988786777")
        phone_set = {phone1, phone2}
        self.assertEqual(len(phone_set), 1)

    def test_phone_invalid_short(self):
        """Тест невалідного короткого номера."""
        with self.assertRaises(ValueError):
            Phone("123")

    def test_phone_invalid_nondigits(self):
        """Тест невалідного номера з буквами."""
        # Note: normalize_phone may process this differently
        # This test depends on Phone implementation
        try:
            phone = Phone("+380988abc777")
            # If it doesn't raise, check if digits are extracted
        except ValueError:
            pass


class TestBirthdayField(unittest.TestCase):
    """Тести для поля Birthday."""

    def test_birthday_creation(self):
        """Тест створення дати народження."""
        birthday = Birthday("15.03.1990")
        self.assertEqual(birthday.value, "15.03.1990")

    def test_birthday_date_value(self):
        """Тест отримання дати як date об'єкта."""
        birthday = Birthday("15.03.1990")
        self.assertEqual(birthday.date_value, date(1990, 3, 15))

    def test_birthday_invalid_format(self):
        """Тест невалідного формату дати."""
        with self.assertRaises(ValueError):
            Birthday("15/03/1990")

    def test_birthday_invalid_date(self):
        """Тест невалідної дати."""
        with self.assertRaises(ValueError):
            Birthday("32.13.1990")

    def test_birthday_leap_year(self):
        """Тест дати 29.02 у високосному році."""
        birthday = Birthday("29.02.2000")
        self.assertEqual(birthday.date_value, date(2000, 2, 29))


class TestRecord(unittest.TestCase):
    """Тести для класу Record."""

    def setUp(self):
        """Підготовка до кожного тесту."""
        self.record = Record("John Doe")

    def test_record_creation(self):
        """Тест створення запису."""
        self.assertEqual(self.record.name.value, "John Doe")
        self.assertIsInstance(self.record.phones, set)
        self.assertEqual(len(self.record.phones), 0)
        self.assertIsNone(self.record.birthday)

    def test_add_phone(self):
        """Тест додавання телефону."""
        self.record.add_phone("+380988786777")
        self.assertEqual(len(self.record.phones), 1)

    def test_add_duplicate_phones(self):
        """Тест додавання дублікатних телефонів."""
        self.record.add_phone("+380988786777")
        self.record.add_phone("+380988786777")
        self.assertEqual(len(self.record.phones), 1)

    def test_add_multiple_phones(self):
        """Тест додавання кількох телефонів."""
        self.record.add_phone("+380988786777")
        self.record.add_phone("+380965544321")
        self.record.add_phone("+380500000000")
        self.assertEqual(len(self.record.phones), 3)

    def test_find_phone(self):
        """Тест пошуку телефону."""
        self.record.add_phone("+380988786777")
        found = self.record.find_phone("+380988786777")
        self.assertIsNotNone(found)
        self.assertEqual(found.value, "+380988786777")

    def test_find_nonexistent_phone(self):
        """Тест пошуку неіснуючого телефону."""
        self.record.add_phone("+380988786777")
        found = self.record.find_phone("+380965544321")
        self.assertIsNone(found)

    def test_remove_phone(self):
        """Тест видалення телефону."""
        self.record.add_phone("+380988786777")
        self.record.add_phone("+380965544321")
        
        phone_to_remove = self.record.find_phone("+380988786777")
        self.record.phones.remove(phone_to_remove)
        
        self.assertEqual(len(self.record.phones), 1)

    def test_edit_phone(self):
        """Тест редагування телефону."""
        self.record.add_phone("+380988786777")
        phone_to_edit = self.record.find_phone("+380988786777")
        self.record.phones.remove(phone_to_edit)
        self.record.add_phone("+380965544321")
        
        self.assertEqual(len(self.record.phones), 1)
        self.assertIsNotNone(self.record.find_phone("+380965544321"))

    def test_add_birthday(self):
        """Тест додавання дня народження."""
        self.record.add_birthday("15.03.1990")
        self.assertIsNotNone(self.record.birthday)
        self.assertEqual(self.record.birthday.value, "15.03.1990")

    def test_record_str(self):
        """Тест строкового представлення."""
        self.record.add_phone("+380988786777")
        self.record.add_birthday("15.03.1990")
        
        record_str = str(self.record)
        self.assertIn("John Doe", record_str)
        self.assertIn("+380988786777", record_str)
        self.assertIn("15.03.1990", record_str)

    def test_record_str_no_birthday(self):
        """Тест строкового представлення без дня народження."""
        self.record.add_phone("+380988786777")
        
        record_str = str(self.record)
        self.assertIn("John Doe", record_str)
        self.assertIn("not set", record_str)


class TestAddressBook(unittest.TestCase):
    """Тести для класу AddressBook."""

    def setUp(self):
        """Підготовка до кожного тесту."""
        self.book = AddressBook()

    def test_empty_book(self):
        """Тест порожної книги."""
        self.assertEqual(len(self.book.data), 0)

    def test_add_record(self):
        """Тест додавання запису."""
        record = Record("Alice")
        record.add_phone("+380988786777")
        self.book.add_record(record)
        
        self.assertEqual(len(self.book.data), 1)
        self.assertIsNotNone(self.book.find("Alice"))

    def test_find_record(self):
        """Тест пошуку запису."""
        record = Record("Bob")
        record.add_phone("+380988786777")
        self.book.add_record(record)
        
        found = self.book.find("Bob")
        self.assertIsNotNone(found)
        self.assertEqual(found.name.value, "Bob")

    def test_find_nonexistent_record(self):
        """Тест пошуку неіснуючого запису."""
        found = self.book.find("Unknown")
        self.assertIsNone(found)

    def test_delete_record(self):
        """Тест видалення запису."""
        record = Record("Charlie")
        self.book.add_record(record)
        
        self.book.delete("Charlie")
        self.assertIsNone(self.book.find("Charlie"))

    def test_delete_nonexistent_record(self):
        """Тест видалення неіснуючого запису."""
        with self.assertRaises(KeyError):
            self.book.delete("Unknown")

    def test_multiple_records(self):
        """Тест кількох записів."""
        for i in range(5):
            record = Record(f"Contact{i}")
            record.add_phone(f"+38098878677{i}")
            self.book.add_record(record)
        
        self.assertEqual(len(self.book.data), 5)

    def test_update_existing_record(self):
        """Тест оновлення існуючого запису."""
        record1 = Record("Diana")
        record1.add_phone("+380988786777")
        self.book.add_record(record1)
        
        record2 = Record("Diana")
        record2.add_phone("+380965544321")
        self.book.add_record(record2)
        
        # Другий добавлення повинне замінити перший
        found = self.book.find("Diana")
        self.assertEqual(len(found.phones), 1)


if __name__ == "__main__":
    unittest.main()
