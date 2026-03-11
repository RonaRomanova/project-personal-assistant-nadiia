"""
Тести для перевірки дедублікації телефонних номерів.

Цей модуль тестує, що Phone об'єкти з однаковими номерами
видаляються при додаванні до set.
"""

import unittest
from contacts import Phone, Record, AddressBook


class TestPhoneEquality(unittest.TestCase):
    """Тести для рівності та хешування Phone об'єктів."""

    def test_phone_equality(self):
        """Тест, що два Phone об'єкти з однаковим номером рівні."""
        phone1 = Phone("+380988786777")
        phone2 = Phone("+380988786777")
        self.assertEqual(phone1, phone2)

    def test_phone_hash_equality(self):
        """Тест, що хеші однакових номерів рівні."""
        phone1 = Phone("+380988786777")
        phone2 = Phone("+380988786777")
        self.assertEqual(hash(phone1), hash(phone2))

    def test_phone_in_set(self):
        """Тест, що однакові номери видаляються в set."""
        phone1 = Phone("+380988786777")
        phone2 = Phone("+380988786777")
        phone_set = {phone1, phone2}
        self.assertEqual(len(phone_set), 1)

    def test_different_phones_in_set(self):
        """Тест, що різні номери зберігаються в set."""
        phone1 = Phone("+380988786777")
        phone2 = Phone("+380965544321")
        phone_set = {phone1, phone2}
        self.assertEqual(len(phone_set), 2)

    def test_phone_inequality(self):
        """Тест, що різні номери не рівні."""
        phone1 = Phone("+380988786777")
        phone2 = Phone("+380965544321")
        self.assertNotEqual(phone1, phone2)


class TestRecordPhoneDeduplication(unittest.TestCase):
    """Тести для дедублікації телефонів у Record."""

    def setUp(self):
        """Підготовка до кожного тесту."""
        self.record = Record("Test User")

    def test_add_duplicate_phones(self):
        """Тест додавання однакових номерів телефону."""
        self.record.add_phone("+380988786777")
        self.record.add_phone("+380988786777")
        self.record.add_phone("+380988786777")
        
        self.assertEqual(len(self.record.phones), 1)

    def test_phones_set_structure(self):
        """Тест, що phones є set."""
        self.assertIsInstance(self.record.phones, set)

    def test_multiple_phones_no_duplicates(self):
        """Тест додавання кількох номерів без дублікатів."""
        self.record.add_phone("+380988786777")
        self.record.add_phone("+380965544321")
        self.record.add_phone("+380988786777")
        self.record.add_phone("+380965544321")
        
        self.assertEqual(len(self.record.phones), 2)

    def test_record_str_no_duplicates(self):
        """Тест, що в __str__ немає дублікатів."""
        self.record.add_phone("+380988786777")
        self.record.add_phone("+380965544321")
        self.record.add_phone("+380988786777")
        
        record_str = str(self.record)
        
        # Підраховуємо кількість появ першого номера
        count = record_str.count("+380988786777")
        self.assertEqual(count, 1, "Номер телефону повинен з'явитися тільки один раз")


class TestAddressBookPhoneDeduplication(unittest.TestCase):
    """Тести для дедублікації в AddressBook."""

    def setUp(self):
        """Підготовка до кожного тесту."""
        self.book = AddressBook()

    def test_book_with_duplicate_phones(self):
        """Тест AddressBook з дублікатними номерами."""
        record = Record("John")
        record.add_phone("+380988786777")
        record.add_phone("+380988786777")
        record.add_phone("+380965544321")
        
        self.book.add_record(record)
        
        found = self.book.find("John")
        self.assertEqual(len(found.phones), 2)

    def test_remove_phone_from_set(self):
        """Тест видалення телефону з set."""
        record = Record("Jane")
        record.add_phone("+380988786777")
        record.add_phone("+380965544321")
        
        phone_to_remove = list(record.phones)[0]
        record.phones.remove(phone_to_remove)
        
        self.assertEqual(len(record.phones), 1)


if __name__ == "__main__":
    unittest.main()
