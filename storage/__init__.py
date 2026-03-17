"""Модуль зберігання для особистого помічника."""

from .file_storage import (
    get_storage_info,
    load_book,
    load_notes,
    save_book,
    save_notes,
)

__all__ = [
    "save_book",
    "load_book",
    "save_notes",
    "load_notes",
    "get_storage_info",
]
