from collections import UserDict
from datetime import date, timedelta

from .constants import UKRAINIAN_DATE_FORMAT
from .record import Record

DEFAULT_DAYS_FOR_BIRTHDAYS = 7


class AddressBook(UserDict):
    """
    Клас для зберігання та керування контактами.
    """

    def add_record(self, record: Record) -> None:
        """
        Додає запис до адресної книги.
        """
        self.data[record.name.value] = record

    def find(self, name: str) -> Record | None:
        """
        Знаходить запис за ім'ям.
        """
        name = name.strip()
        if name in self.data:
            return self.data[name]

        for key, record in self.data.items():
            if key.lower() == name.lower():
                return record
        return None

    def search_by_name(self, partial_name: str) -> list[Record]:
        """
        Знаходить записи, ім'я яких містить заданий рядок
        (без урахування регістру).
        """
        return [
            record
            for name, record in self.data.items()
            if partial_name.lower() in name.lower()
        ]

    def search(self, query: str) -> list[Record]:
        """
        Знаходить записи за повнотекстовим пошуком по всіх полях.
        """
        return [
            record for record in self.data.values() if record.matches(query)
        ]

    def delete(self, name: str) -> None:
        """
        Видаляє запис за ім'ям.
        """
        name = name.strip()
        if name in self.data:
            del self.data[name]
            return

        for key in list(self.data.keys()):
            if key.lower() == name.lower():
                del self.data[key]
                return

        raise KeyError

    @staticmethod
    def _get_birthday_for_year(birthday: str, year: int) -> date:
        """
        Повертає дату дня народження для вказаного року.
        Якщо дата 29.02 і рік не високосний, повертає 28.02.
        """
        try:
            return birthday.replace(year=year)
        except ValueError:
            return birthday.replace(year=year, day=28)

    def get_upcoming_birthdays(
        self, days=DEFAULT_DAYS_FOR_BIRTHDAYS
    ) -> list[dict[str, str]]:
        """
        Повертає список користувачів, яких потрібно
        привітати протягом вказаного періоду (за замовчуванням 7 днів).
        """
        today = date.today()
        upcoming_birthdays = []

        for record in self.data.values():
            if record.birthday is None:
                continue

            birthday_this_year = self._get_birthday_for_year(
                record.birthday.date_value, today.year
            )

            if birthday_this_year < today:
                birthday_this_year = self._get_birthday_for_year(
                    record.birthday.date_value, today.year + 1
                )

            days_difference = (birthday_this_year - today).days

            if 0 <= days_difference <= days:
                congratulation_date = birthday_this_year

                if congratulation_date.weekday() >= 5:
                    days_to_monday = 7 - congratulation_date.weekday()
                    congratulation_date = congratulation_date + timedelta(
                        days=days_to_monday
                    )

                bday_date = record.birthday.date_value
                upcoming_birthdays.append(
                    {
                        "name": record.name.value,
                        "original_birthday": bday_date.strftime(
                            UKRAINIAN_DATE_FORMAT
                        ),
                        "age": birthday_this_year.year - bday_date.year,
                        "congratulation_date": congratulation_date.strftime(
                            UKRAINIAN_DATE_FORMAT
                        ),
                    }
                )

        return upcoming_birthdays
