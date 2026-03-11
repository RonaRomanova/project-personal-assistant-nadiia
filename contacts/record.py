from .fields import Email, Name, Phone, Birthday   

class Record:
    """
    Клас для зберігання інформації про контакт:
    ім'я, список телефонів, список email-адрес і день народження.
    """

    def __init__(self, name: str) -> None:
        self.name = Name(name)
        self.phones = set()
        self.emails = set()
        self.birthday: Birthday | None = None

    def add_phone(self, phone: str) -> None:
        """
        Додає телефон до контакту.
        """
        self.phones.add(Phone(phone))

    def remove_phone(self, phone: str) -> None:
        """
        Видаляє телефон із контакту.
        """
        phone_to_remove = self.find_phone(phone)

        if phone_to_remove:
            self.phones.remove(phone_to_remove)
        else:
            raise ValueError("Номер телефону не знайдено.")

    def edit_phone(self, old_phone: str, new_phone: str) -> None:
        """
        Замінює старий телефон на новий.
        """
        phone_to_edit = self.find_phone(old_phone)

        if phone_to_edit:
            self.phones.remove(phone_to_edit)
            self.phones.add(Phone(new_phone))
        else:
            raise ValueError("Номер телефону не знайдено.")

    def find_phone(self, phone: str) -> Phone | None:
        """
        Шукає телефон у контакті.
        """
        for contact_phone in self.phones:
            if contact_phone.value == phone:
                return contact_phone
        return None

    def add_birthday(self, birthday: str) -> None:
        """
        Додає день народження до контакту.
        """
        self.birthday = Birthday(birthday)

    def __str__(self) -> str:
        phones_str = "; ".join(phone.value for phone in self.phones)
        birthday_str = self.birthday.value if self.birthday else "not set"
        return (
            f"Contact name: {self.name.value}, "
            f"phones: {phones_str}, "
            f"birthday: {birthday_str}"
        )