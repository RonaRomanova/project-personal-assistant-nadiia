import pickle

from contacts import AddressBook

DEFAULT_FILENAME = "addressbook.pkl"

def save_data(book: AddressBook, filename: str = DEFAULT_FILENAME) -> None:
    """
    Зберігає адресну книгу у файл за допомогою pickle.
    """
    with open(filename, "wb") as file:
        pickle.dump(book, file)


def load_data(filename: str = DEFAULT_FILENAME) -> AddressBook:
    """
    Завантажує адресну книгу з файлу за допомогою pickle.
    Якщо файл не знайдено, повертає нову порожню адресну книгу.
    """
    try:
        with open(filename, "rb") as file:
            return pickle.load(file)
    except (FileNotFoundError, AttributeError):
        return AddressBook()
