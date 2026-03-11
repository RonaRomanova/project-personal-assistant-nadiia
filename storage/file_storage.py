import pickle

from contacts import AddressBook

def save_data(book: AddressBook, filename: str = "addressbook.pkl") -> None:
    """
    Зберігає адресну книгу у файл за допомогою pickle.
    """
    with open(filename, "wb") as file:
        pickle.dump(book, file)


def load_data(filename: str = "addressbook.pkl") -> AddressBook:
    """
    Завантажує адресну книгу з файлу за допомогою pickle.
    Якщо файл не знайдено, повертає нову порожню адресну книгу.
    """
    try:
        with open(filename, "rb") as file:
            return pickle.load(file)
    except (FileNotFoundError, AttributeError):
        return AddressBook()
