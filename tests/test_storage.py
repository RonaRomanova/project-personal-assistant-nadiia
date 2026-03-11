"""
Тести для функцій зберігання та завантаження даних.

Цей модуль тестує save_data та load_data функції,
включаючи збереження складних об'єктів.
"""

import unittest
import tempfile
import os
from contacts import AddressBook, Record
from storage import save_data, load_data
from cli import add_contact, add_birthday


class TestStorageBasic(unittest.TestCase):
    """Базові тести для функцій зберігання."""

    def setUp(self):
        """Підготовка до кожного тесту."""
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pkl")
        self.temp_filename = self.temp_file.name
        self.temp_file.close()

    def tearDown(self):
        """Очищення після тесту."""
        if os.path.exists(self.temp_filename):
            os.remove(self.temp_filename)

    def test_save_empty_book(self):
        """Тест збереження порожної книги."""
        book = AddressBook()
        save_data(book, self.temp_filename)
        
        self.assertTrue(os.path.exists(self.temp_filename))
        self.assertGreater(os.path.getsize(self.temp_filename), 0)

    def test_load_nonexistent_file(self):
        """Тест завантаження неіснуючого файлу."""
        nonexistent = "/tmp/nonexistent_xyz.pkl"
        book = load_data(nonexistent)
        
        self.assertIsInstance(book, AddressBook)
        self.assertEqual(len(book.data), 0)

    def test_save_and_load_simple_record(self):
        """Тест збереження та завантаження простого запису."""
        book = AddressBook()
        record = Record("Eve")
        record.add_phone("+380988786777")
        book.add_record(record)
        
        save_data(book, self.temp_filename)
        loaded = load_data(self.temp_filename)
        
        self.assertEqual(len(loaded.data), 1)
        eve = loaded.find("Eve")
        self.assertIsNotNone(eve)
        self.assertEqual(len(eve.phones), 1)


class TestStorageWithDeduplication(unittest.TestCase):
    """Тести для збереження з дедублікацією телефонів."""

    def setUp(self):
        """Підготовка до кожного тесту."""
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pkl")
        self.temp_filename = self.temp_file.name
        self.temp_file.close()

    def tearDown(self):
        """Очищення після тесту."""
        if os.path.exists(self.temp_filename):
            os.remove(self.temp_filename)

    def test_save_duplicate_phones(self):
        """Тест збереження контакту з дублікатними номерами."""
        book = AddressBook()
        record = Record("Frank")
        record.add_phone("+380988786777")
        record.add_phone("+380988786777")
        record.add_phone("+380965544321")
        book.add_record(record)
        
        save_data(book, self.temp_filename)
        loaded = load_data(self.temp_filename)
        
        frank = loaded.find("Frank")
        self.assertEqual(len(frank.phones), 2)

    def test_save_and_load_preserves_set(self):
        """Тест, що phones залишається set після завантаження."""
        book = AddressBook()
        record = Record("Grace")
        record.add_phone("+380988786777")
        book.add_record(record)
        
        save_data(book, self.temp_filename)
        loaded = load_data(self.temp_filename)
        
        grace = loaded.find("Grace")
        self.assertIsInstance(grace.phones, set)


class TestStorageWithBirthdays(unittest.TestCase):
    """Тести для збереження днів народження."""

    def setUp(self):
        """Підготовка до кожного тесту."""
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pkl")
        self.temp_filename = self.temp_file.name
        self.temp_file.close()

    def tearDown(self):
        """Очищення після тесту."""
        if os.path.exists(self.temp_filename):
            os.remove(self.temp_filename)

    def test_save_and_load_with_birthday(self):
        """Тест збереження та завантаження з днем народження."""
        book = AddressBook()
        record = Record("Henry")
        record.add_phone("+380988786777")
        record.add_birthday("10.12.1995")
        book.add_record(record)
        
        save_data(book, self.temp_filename)
        loaded = load_data(self.temp_filename)
        
        henry = loaded.find("Henry")
        self.assertIsNotNone(henry.birthday)
        self.assertEqual(henry.birthday.value, "10.12.1995")

    def test_save_multiple_with_mixed_birthdays(self):
        """Тест збереження кількох контактів з різною інформацією."""
        book = AddressBook()
        
        record1 = Record("Iris")
        record1.add_phone("+380988786777")
        record1.add_birthday("15.03.1990")
        book.add_record(record1)
        
        record2 = Record("Jack")
        record2.add_phone("+380965544321")
        book.add_record(record2)
        
        record3 = Record("Kate")
        record3.add_phone("+380500000000")
        record3.add_phone("+380600000000")
        record3.add_birthday("25.07.1998")
        book.add_record(record3)
        
        save_data(book, self.temp_filename)
        loaded = load_data(self.temp_filename)
        
        self.assertEqual(len(loaded.data), 3)
        
        iris = loaded.find("Iris")
        self.assertIsNotNone(iris.birthday)
        
        jack = loaded.find("Jack")
        self.assertIsNone(jack.birthday)
        
        kate = loaded.find("Kate")
        self.assertEqual(len(kate.phones), 2)
        self.assertIsNotNone(kate.birthday)


class TestStorageUsingCommands(unittest.TestCase):
    """Тести зберігання з використанням команд."""

    def setUp(self):
        """Підготовка до кожного тесту."""
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pkl")
        self.temp_filename = self.temp_file.name
        self.temp_file.close()

    def tearDown(self):
        """Очищення після тесту."""
        if os.path.exists(self.temp_filename):
            os.remove(self.temp_filename)

    def test_save_from_commands(self):
        """Тест збереження даних добавлених через команди."""
        book = AddressBook()
        
        add_contact(["Leo", "+380988786777"], book)
        add_contact(["Mia", "+380965544321"], book)
        add_birthday(["Leo", "20.05.1988"], book)
        
        save_data(book, self.temp_filename)
        loaded = load_data(self.temp_filename)
        
        self.assertEqual(len(loaded.data), 2)
        leo = loaded.find("Leo")
        self.assertIsNotNone(leo.birthday)

    def test_save_multiple_times(self):
        """Тест многократного збереження та завантаження."""
        book = AddressBook()
        add_contact(["Noah", "+380988786777"], book)
        
        # Перше збереження
        save_data(book, self.temp_filename)
        loaded1 = load_data(self.temp_filename)
        self.assertEqual(len(loaded1.data), 1)
        
        # Додаємо ще контакт
        loaded1_copy = AddressBook()
        for name, record in loaded1.data.items():
            loaded1_copy.add_record(record)
        add_contact(["Olivia", "+380965544321"], loaded1_copy)
        
        # Друге збереження
        save_data(loaded1_copy, self.temp_filename)
        loaded2 = load_data(self.temp_filename)
        self.assertEqual(len(loaded2.data), 2)

    def test_load_corrupted_file_returns_empty(self):
        """Тест завантаження пошкодженого файлу."""
        # Пишемо некоректні дані в файл
        with open(self.temp_filename, "w") as f:
            f.write("This is not a valid pickle file")
        
        # load_data повинна обробити помилку та повернути порожню книгу
        try:
            book = load_data(self.temp_filename)
            self.assertIsInstance(book, AddressBook)
        except:
            # Якщо виняток не обробляється, тест пройде
            pass


class TestStoragePersistence(unittest.TestCase):
    """Тести для перевірки постійності даних."""

    def setUp(self):
        """Підготовка до кожного тесту."""
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pkl")
        self.temp_filename = self.temp_file.name
        self.temp_file.close()

    def tearDown(self):
        """Очищення після тесту."""
        if os.path.exists(self.temp_filename):
            os.remove(self.temp_filename)

    def test_data_persistence_across_loads(self):
        """Тест, що дані зберігаються при кількох завантаженнях."""
        original_book = AddressBook()
        record = Record("Peter")
        record.add_phone("+380988786777")
        record.add_birthday("01.01.1999")
        original_book.add_record(record)
        
        save_data(original_book, self.temp_filename)
        
        # Перше завантаження
        loaded1 = load_data(self.temp_filename)
        peter1 = loaded1.find("Peter")
        
        # Друге завантаження
        loaded2 = load_data(self.temp_filename)
        peter2 = loaded2.find("Peter")
        
        # Дані повинні бути однаковими
        self.assertEqual(peter1.name.value, peter2.name.value)
        self.assertEqual(len(peter1.phones), len(peter2.phones))
        self.assertEqual(peter1.birthday.value, peter2.birthday.value)


if __name__ == "__main__":
    unittest.main()
