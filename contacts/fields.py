from datetime import datetime
import re
from utils.helpers import parse_date

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
         # Порівнюємо об'єкти Phone за їх нормалізованим значенням
        if isinstance(other, Phone):
            return self.value == other.value
        return False

    def __hash__(self) -> int:
         # Хешуємо об'єкт Phone на основі його нормалізованого значення, 
         # щоб забезпечити коректну роботу в множинах та як ключі словника
        return hash(self.value)

    @staticmethod
    def normalize_phone(phone_number: str) -> str:
        # Видаляємо всі символи, крім цифр та символу '+'
        # Це для того, щоб зберегти можливий + на початку, але потім ми все одно беремо тільки цифри.
        cleaned = re.sub(r'[^\d\+]', '', phone_number)
        
        # Витягуємо всі цифри (ігноруємо +)
        digits = re.sub(r'\D', '', cleaned)
        
        # Перевірка мінімальної кількості цифр
        if len(digits) < 9:
            raise ValueError("Номер телефону має містити не менше 9 цифр (без урахування коду країни).")
        
        # Перевірка максимальної кількості цифр
        if len(digits) > 12:
            raise ValueError("Номер телефону має містити не більше 12 цифр в форматі +380XXXXXXXXX (введено більше).")
        
        # Обробка залежно від кількості цифр
        if len(digits) == 12:
            # 12 цифр - це номер з кодом країни (без +)
            if not digits.startswith('380'):
                raise ValueError("Номер з 12 цифр має починатися з коду України 380.")
            normalized = '+' + digits  # додаємо + на початок
        else:
            # Від 9 до 11 цифр - локальний номер. Перевірка відповідності стандартам
            if len(digits) == 10 and not digits.startswith('0'):
                raise ValueError("Номер з 10 цифр має починатися з 0 (наприклад, 0971234567).")
            if len(digits) == 11 and not digits.startswith('80'):
                raise ValueError("Номер з 11 цифр має починатися з 80 (наприклад, 80971234567).")
            
            # Беремо останні 9 цифр (відкидаємо префікс 0 або 80)
            local_number = digits[-9:]
            normalized = '+380' + local_number
        
        # Перевірка, що результат має рівно 13 символів
        if len(normalized) != 13:
            # Перевірка на всяк випадок)
            raise ValueError(f"Внутрішня помилка нормалізації: отримано {len(normalized)} символів замість 13.")
        
        return normalized
    

class Email(Field):
    """
    Клас для зберігання email-адреси.
    З урахуванням базової нормалізації та валідації (наявність локальної частини та домену, правильний формат "user@domain.com").
    """

    def __init__(self, value: str) -> None:
        normalized = self.normalize_email(value)
        super().__init__(normalized)

    def __eq__(self, other) -> bool:
         # Порівнюємо об'єкти Email за їх нормалізованим значенням
        if isinstance(other, Email):
            return self.value == other.value
        return False

    def __hash__(self) -> int:
         # Хешуємо об'єкт Email на основі його нормалізованого значення, 
         # щоб забезпечити коректну роботу в множинах та як ключі словника
        return hash(self.value)

    @staticmethod
    def normalize_email(email: str) -> str:
        # 1. Видаляємо пробіли на початку і в кінці
        email = email.strip()
        
        # 2. Перевірка наявності '@'
        if '@' not in email:
            raise ValueError("Email має містити символ '@' в форматі 'user@domain.com'.")
        
        # 3. Розділяємо на локальну частину та домен
        local, domain = email.rsplit('@', 1)
        
        # 4. Перевірка, що локальна частина не порожня
        if not local:
            raise ValueError("Email має містити локальну частину перед '@' в форматі 'user@domain.com'.")
        
        # 5. Перевірка, що домен не порожній і містить хоча б одну крапку
        if not domain or '.' not in domain:
            raise ValueError("Email має містити домен з крапкою в форматі 'user@domain.com'.")
        
        # 6. Нормалізація: домен переводимо в нижній регістр згідно стандарту, локальну частину залишаємо без змін (може бути чутлива до регістру)
        domain = domain.lower()
        
        # 7.Збираємо email назад
        normalized = f"{local}@{domain}"
        
        # 8. Додаткова перевірка на допустимі символи (опціонально)
        #    Дозволені літери, цифри, крапки, дефіси, підкреслення тощо.
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', normalized):
            raise ValueError("Email містить неприпустимі символи або неправильний формат.")
        
        return normalized    


class Birthday(Field):
    """
    Клас для зберігання дня народження.
    Формат: DD.MM.YYYY
    """

    def __init__(self, value: str) -> None:
        try:
            birthday_date = datetime.strptime(parse_date(value), "%Y-%m-%d").date()     
            # parse_date(value)
        except ValueError:
            raise ValueError("Невірний формат дати. Використовуйте YYYY-MM-DD")

        super().__init__(value)
        self.date_value = birthday_date
