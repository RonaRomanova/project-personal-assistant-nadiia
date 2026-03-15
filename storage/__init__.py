"""Модуль зберігання для особистого помічника."""

from .file_storage import load_book, load_notes, save_book, save_notes

__all__ = ["save_book", "load_book", "save_notes", "load_notes"]
