import json
from pathlib import Path

from contacts import AddressBook
from contacts.record import Record
from notes import Notebook
from notes.note import Note
from utils.logger import get_logger

logger = get_logger()

DEFAULT_FILENAME = "addressbook.json"


def save_book(book: AddressBook, filename: str = DEFAULT_FILENAME) -> None:
    """
    Зберігає адресну книгу у файл у форматі JSON.
    """
    data = []
    for record in book.data.values():
        data.append(
            {
                "name": record.name.value,
                "address": record.address.value if record.address else None,
                "phones": [p.value for p in record.phones],
                "emails": [e.value for e in record.emails],
                "birthday": record.birthday.value if record.birthday else None,
            }
        )
    try:
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
        logger.info(f"Address book saved to {filename}")
    except Exception as e:
        logger.error(f"Error saving address book: {e}", exc_info=True)


def load_book(filename: str = DEFAULT_FILENAME) -> AddressBook:
    """
    Завантажує адресну книгу з файлу у форматі JSON.
    Якщо файл не знайдено, повертає нову порожню адресну книгу.
    """
    book = AddressBook()
    try:
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)
            for item in data:
                record = Record(item["name"])
                if item.get("address"):
                    record.edit_address(item["address"])
                for phone in item.get("phones", []):
                    try:
                        record.add_phone(phone)
                    except ValueError:
                        pass
                for email in item.get("emails", []):
                    try:
                        record.add_email(email)
                    except ValueError:
                        pass
                if item.get("birthday"):
                    try:
                        record.edit_birthday(item["birthday"])
                    except ValueError:
                        pass
                book.add_record(record)
        logger.info(
            f"Address book loaded from {filename}. Records: {len(book.data)}"
        )
    except FileNotFoundError:
        logger.info(f"Address book file {filename} not found.")
    except Exception as e:
        logger.error(f"Error loading address book: {e}", exc_info=True)
        pass
    return book


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
    try:
        NOTES_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2))
        logger.info(f"Notes saved to {NOTES_FILE}")
    except Exception as e:
        logger.error(f"Error saving notes: {e}", exc_info=True)


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
    logger.info(
        f"Notes loaded from {NOTES_FILE}. Count: {len(notebook._notes)}"
    )
    return notebook


def get_storage_info() -> dict[str, str]:
    """Повертає абсолютні шляхи до файлів зберігання у форматі URL."""
    return {
        "addressbook": f"file://{Path(DEFAULT_FILENAME).absolute()}",
        "notes": f"file://{NOTES_FILE.absolute()}",
    }
