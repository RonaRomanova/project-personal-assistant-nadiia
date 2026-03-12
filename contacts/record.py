from .fields import Address, Email, Name, Phone, Birthday


class Record:
    """
    Клас для зберігання інформації про контакт:
    ім'я, адреса, список телефонів, список email-адрес і день народження.
    """

    def __init__(self, name: str) -> None:
        self.name = Name(name)
        self.address: Address | None = None
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

    def add_email(self, email: str) -> None:
        """
        Додає email до контакту.
        """
        self.emails.add(Email(email))

    def remove_email(self, email: str) -> None:
        """
        Видаляє email із контакту.
        """
        email_to_remove = self.find_email(email)

        if email_to_remove:
            self.emails.remove(email_to_remove)
        else:
            raise ValueError("Email не знайдено.")

    def edit_email(self, old_email: str, new_email: str) -> None:
        """
        Замінює старий email на новий.
        """
        email_to_edit = self.find_email(old_email)

        if email_to_edit:
            self.emails.remove(email_to_edit)
            self.emails.add(Email(new_email))
        else:
            raise ValueError("Email не знайдено.")

    def find_email(self, email: str) -> Email | None:
        """
        Шукає email у контакті.
        """
        for contact_email in self.emails:
            if contact_email.value == email:
                return contact_email
        return None

    def add_address(self, address: str) -> None:
        """
        Додає адресу до контакту.
        """
        self.address = Address(address)

    def add_birthday(self, birthday: str) -> None:
        """
        Додає день народження до контакту.
        """
        self.birthday = Birthday(birthday)

    def __str__(self) -> str:
        phones_str = "; ".join(p.value for p in self.phones) if self.phones else "не вказано"
        emails_str = "; ".join(e.value for e in self.emails) if self.emails else "не вказано"
        birthday_str = self.birthday.value if self.birthday else "не вказано"
        address_str = self.address.value if self.address else "не вказано"

        return (
            f"========================================\n"
            f"  Ім'я: {self.name.value}\n"
            f"  Адреса: {address_str}\n"
            f"  Телефони: {phones_str}\n"
            f"  Emails: {emails_str}\n"
            f"  День народження: {birthday_str}"
            
        )