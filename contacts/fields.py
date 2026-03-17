import re
from datetime import datetime

from utils.helpers import parse_date

from .constants import (
    DATE_FORMAT,
    DIGITS_ONLY_REGEX,
    EMAIL_REGEX,
    MAX_PHONE_DIGITS,
    MIN_PHONE_DIGITS,
    NORMALIZED_PHONE_LENGTH,
    PHONE_REGEX,
    UKRAINE_COUNTRY_CODE,
)


class Field:
    """
    Базовий клас для полів запису.
    """

    def __init__(self, value: str) -> None:
        self.value = value

    def __str__(self) -> str:
        return str(self.value)


class Name(Field):
    """
    Клас для зберігання імені контакту.
    """

    pass


class Address(Field):
    """
    Клас для зберігання адреси.
    """

    pass


class Phone(Field):
    """
    Клас для зберігання номера телефону.
    Після нормалізації номер має формат +380XXXXXXXXX (13 символів).
    """

    def __init__(self, value: str) -> None:
        normalized = self.normalize_phone(value)
        super().__init__(normalized)

    def __eq__(self, other) -> bool:
        if isinstance(other, Phone):
            return self.value == other.value
        return False

    def __hash__(self) -> int:
        return hash(self.value)

    @staticmethod
    def normalize_phone(phone_number: str) -> str:
        """
        Нормалізує номер телефону.
        """
        cleaned = re.sub(PHONE_REGEX, "", phone_number)
        digits = re.sub(DIGITS_ONLY_REGEX, "", cleaned)

        if len(digits) < MIN_PHONE_DIGITS:
            raise ValueError(
                f"Номер телефону має містити не менше {MIN_PHONE_DIGITS} цифр "
                "(без урахування коду країни)."
            )
        if len(digits) > MAX_PHONE_DIGITS:
            raise ValueError(
                f"Номер телефону має містити не більше "
                f"{MAX_PHONE_DIGITS} цифр в форматі "
                f"+{UKRAINE_COUNTRY_CODE}XXXXXXXXX."
            )

        if len(digits) == 12:
            if not digits.startswith(UKRAINE_COUNTRY_CODE):
                raise ValueError(
                    f"Номер з 12 цифр має починатися з коду "
                    f"{UKRAINE_COUNTRY_CODE}."
                )
            normalized = "+" + digits
        else:
            if len(digits) == 9 and digits.startswith("0"):
                raise ValueError(
                    "Локальний номер з 9 цифр не повинен починатися з 0."
                )
            if len(digits) == 10 and not digits.startswith("0"):
                raise ValueError(
                    "Номер з 10 цифр має починатися з 0 "
                    "(наприклад, 0971234567)."
                )
            if len(digits) == 11 and not digits.startswith("80"):
                raise ValueError(
                    "Номер з 11 цифр має починатися з 80 "
                    "(наприклад, 80971234567)."
                )

            local_number = digits[-9:]
            normalized = f"+{UKRAINE_COUNTRY_CODE}{local_number}"

        if len(normalized) != NORMALIZED_PHONE_LENGTH:
            raise ValueError(
                f"Внутрішня помилка нормалізації: отримано "
                f"{len(normalized)} символів замість "
                f"{NORMALIZED_PHONE_LENGTH}."
            )

        return normalized


class Email(Field):
    """
    Клас для зберігання email-адреси.
    """

    def __init__(self, value: str) -> None:
        normalized = self.normalize_email(value)
        super().__init__(normalized)

    def __eq__(self, other) -> bool:
        if isinstance(other, Email):
            return self.value == other.value
        return False

    def __hash__(self) -> int:
        return hash(self.value)

    @staticmethod
    def normalize_email(email: str) -> str:
        email = email.strip()

        if "@" not in email:
            raise ValueError(
                "Email має містити символ '@' в форматі 'user@domain.com'."
            )

        local, domain = email.rsplit("@", 1)

        if not local:
            raise ValueError(
                "Email має містити локальну частину перед '@' "
                "в форматі 'user@domain.com'."
            )

        if not domain or "." not in domain:
            raise ValueError(
                "Email має містити домен з крапкою "
                "в форматі 'user@domain.com'."
            )

        domain = domain.lower()
        normalized = f"{local}@{domain}"

        if not re.match(EMAIL_REGEX, normalized):
            raise ValueError(
                "Email містить неприпустимі символи або неправильний формат."
            )

        return normalized


class Birthday(Field):
    """
    Клас для зберігання дня народження.
    Формат: YYYY-MM-DD
    """

    def __init__(self, value: str) -> None:
        try:
            birthday_date = datetime.strptime(
                parse_date(value), DATE_FORMAT
            ).date()
        except (ValueError, TypeError):
            raise ValueError(
                f"Невірний формат дати. Використовуйте {DATE_FORMAT}"
            )

        super().__init__(value)
        self.date_value = birthday_date
