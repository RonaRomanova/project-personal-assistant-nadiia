from datetime import datetime

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


class Phone(Field):
    """
    Клас для зберігання номера телефону.
    Номер має складатися рівно з 10 цифр.
    """

    def __init__(self, value: str) -> None:
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Номер телефону має складатися рівно з 10 цифр.")
        super().__init__(value)


class Birthday(Field):
    """
    Клас для зберігання дня народження.
    Формат: DD.MM.YYYY
    """

    def __init__(self, value: str) -> None:
        try:
            birthday_date = datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("Невірний формат дати. Використовуйте DD.MM.YYYY")

        super().__init__(value)
        self.date_value = birthday_date
