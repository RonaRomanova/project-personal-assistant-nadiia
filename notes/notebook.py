from typing import Dict, List

from .note import Note


class Notebook:
    """
    Клас для зберігання та керування нотатками.
    """

    def __init__(self) -> None:
        """Ініціалізує порожній блокнот."""
        self._notes: Dict[int, Note] = {}
        self._next_id: int = 1

    def add_note(self, text: str, tags: list[str] | None = None) -> Note:
        """Додає нову нотатку з текстом і необов'язковими тегами."""
        note = Note(id=self._next_id, text=text, tags=tags or [])
        self._notes[self._next_id] = note
        self._next_id += 1
        return note

    def delete_note(self, note_id: int) -> bool:
        """Видаляє нотатку за її ідентифікатором."""
        return self._notes.pop(note_id, None) is not None

    def edit_note(self, note_id: int, new_text: str) -> bool:
        """Редагує нотатку за її ідентифікатором."""
        note = self._notes.get(note_id)
        if not note:
            return False
        note.text = new_text
        return True

    def find(self, query: str) -> List[Note]:
        """Пошук нотаток за текстом або тегами (повнотекстовий)."""
        return [n for n in self._notes.values() if n.matches(query)]

    def search_by_tag(self, tag_query: str) -> List[Note]:
        """Пошук нотаток тільки за тегами."""
        q = tag_query.lower()
        return [
            n
            for n in self._notes.values()
            if any(q in t.lower() for t in n.tags)
        ]

    def search_by_text(self, text_query: str) -> List[Note]:
        """Пошук нотаток тільки за текстом."""
        q = text_query.lower()
        return [n for n in self._notes.values() if q in n.text.lower()]

    def all_notes(self) -> List[Note]:
        """Повертає всі нотатки."""
        return list(self._notes.values())
