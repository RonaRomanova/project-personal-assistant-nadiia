import pickle

from contacts import AddressBook
from notes import Notebook
import json
from pathlib import Path
from notes.note import Note

DEFAULT_FILENAME = "addressbook.pkl"

def save_book(book: AddressBook, filename: str = DEFAULT_FILENAME) -> None:
    """
    Зберігає адресну книгу у файл за допомогою pickle.
    """
    with open(filename, "wb") as file:
        pickle.dump(book, file)


def load_book(filename: str = DEFAULT_FILENAME) -> AddressBook:
    """
    Завантажує адресну книгу з файлу за допомогою pickle.
    Якщо файл не знайдено, повертає нову порожню адресну книгу.
    """
    try:
        with open(filename, "rb") as file:
            return pickle.load(file)
    except (FileNotFoundError, AttributeError):
        return AddressBook()



NOTES_FILE = Path("notes.json")

def save_notes(notebook: Notebook) -> None:
    """Зберігає нотатки у файл у форматі JSON."""
    data = [
        {
            "id": n.id,
            "text": n.text,
            "tags": n.tags,
            "created_at": n.created_at.isoformat(),
        }
        for n in notebook.all_notes()
    ]
    NOTES_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2))

def load_notes() -> Notebook:
    """Завантажує нотатки з файлу, якщо він існує."""
    if not NOTES_FILE.exists():
        return Notebook()
    notebook = Notebook()
    data = json.loads(NOTES_FILE.read_text())
    max_id = 0
    for item in data:
        note = Note(
            id=item["id"],
            text=item["text"],
            tags=item.get("tags", []),
        )
        notebook._notes[note.id] = note
        max_id = max(max_id, note.id)
    notebook._next_id = max_id + 1
    return notebook