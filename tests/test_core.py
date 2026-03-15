import pytest
from contacts.address_book import AddressBook
from contacts.record import Record
from notes.notebook import Notebook

def test_add_contact():
    book = AddressBook()
    record = Record("John Doe")
    record.add_phone("0991234567")
    book.add_record(record)
    assert book.find("John Doe") is not None
    assert book.find("John Doe").name.value == "John Doe"

def test_edit_phone():
    record = Record("John Doe")
    record.add_phone("0991234567")
    record.edit_phone("0991234567", "0977654321")
    assert "+380977654321" in [p.value for p in record.phones]
    assert "+380991234567" not in [p.value for p in record.phones]

def test_add_note():
    notebook = Notebook()
    note = notebook.add_note("Test note", ["tag1", "tag2"])
    assert note.text == "Test note"
    assert "tag1" in note.tags
    assert len(notebook.all_notes()) == 1

def test_find_note():
    notebook = Notebook()
    notebook.add_note("Python is great", ["python"])
    notebook.add_note("Weather is nice", ["weather"])
    results = notebook.find("python")
    assert len(results) == 1
    assert "Python is great" in results[0].text
