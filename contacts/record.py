from .fields import Address, Birthday, Email, Name, Phone
from .constants import NOT_SPECIFIED


class Record:
    """
    Клас для зберігання інформації про контакт.
    """

    def __init__(self, name: str) -> None:
        self.name = Name(name)
        self.address: Address | None = None
        self.phones = set()
        self.emails = set()
        self.birthday: Birthday | None = None

    def add_phone(self, phone: str) -> None:
        self.phones.add(Phone(phone))

    def remove_phone(self, phone: str) -> None:
        normalized = Phone(phone).value
        phone_to_remove = self.find_item(self.phones, normalized)
        if phone_to_remove:
            self.phones.remove(phone_to_remove)
        else:
            raise ValueError("Номер телефону не знайдено.")

    def edit_phone(self, old_phone: str, new_phone: str) -> None:
        normalized_old = Phone(old_phone).value
        phone_to_edit = self.find_item(self.phones, normalized_old)
        if phone_to_edit:
            self.phones.remove(phone_to_edit)
            self.phones.add(Phone(new_phone))
        else:
            raise ValueError("Номер телефону не знайдено.")

    def add_email(self, email: str) -> None:
        self.emails.add(Email(email))

    def remove_email(self, email: str) -> None:
        normalized = Email(email).value
        email_to_remove = self.find_item(self.emails, normalized)
        if email_to_remove:
            self.emails.remove(email_to_remove)
        else:
            raise ValueError("Email не знайдено.")

    def edit_email(self, old_email: str, new_email: str) -> None:
        normalized_old = Email(old_email).value
        email_to_edit = self.find_item(self.emails, normalized_old)
        if email_to_edit:
            self.emails.remove(email_to_edit)
            self.emails.add(Email(new_email))
        else:
            raise ValueError("Email не знайдено.")

    def find_item(self, collection, value):
        """Знаходить об'єкт у колекції за його значенням value."""
        for item in collection:
            if item.value == value:
                return item
        return None

    def edit_birthday(self, birthday: str) -> None:
        self.birthday = Birthday(birthday)

    def edit_address(self, address: str) -> None:
        self.address = Address(address)

    def matches(self, query: str) -> bool:
        """Пошук по всім полям контакту."""
        q = query.lower()
        if q in self.name.value.lower():
            return True
        if any(q in p.value.lower() for p in self.phones):
            return True
        if any(q in e.value.lower() for e in self.emails):
            return True
        if self.address and q in self.address.value.lower():
            return True
        if self.birthday and q in self.birthday.value.lower():
            return True
        return False

    def __str__(self) -> str:
        phones_str = (
            "; ".join(p.value for p in self.phones)
            if self.phones
            else NOT_SPECIFIED
        )
        emails_str = (
            "; ".join(e.value for e in self.emails)
            if self.emails
            else NOT_SPECIFIED
        )
        birthday_str = self.birthday.value if self.birthday else NOT_SPECIFIED
        address_str = self.address.value if self.address else NOT_SPECIFIED

        return (
            f"{'=' * 40}\n"
            f"  Ім'я: {self.name.value}\n"
            f"  Адреса: {address_str}\n"
            f"  Телефони: {phones_str}\n"
            f"  Emails: {emails_str}\n"
            f"  День народження: {birthday_str}"
        )
