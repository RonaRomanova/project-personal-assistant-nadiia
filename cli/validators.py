import re

def get_usage_from_doc(func):
    """
    Допоміжна функція для витягування формату команди з докстрінгу.
    """
    if not func.__doc__:
        return "Перевірте формат команди за допомогою 'help'."
    
    # Шукаємо рядок, що містить "Формат:"
    match = re.search(r"Формат: .*", func.__doc__, re.IGNORECASE)
    if match:
        return f"Очікується: {match.group(0)}"
    
    return "Перевірте формат команди за допомогою 'help'."

def input_error(func):
    """
    Декоратор для централізованої обробки помилок введення.
    Він перехоплює основні помилки та намагається надати
    користувачу максимально корисну інформацію, використовуючи докстрінг функції.
    """

    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as error:
            # Помилки валідації (неправильний телефон, дата) або розпакування
            if "unpack" in str(error):
                return f"Неправильна кількість аргументів. {get_usage_from_doc(func)}"
            return f"Помилка даних: {error}"
        except KeyError:
            # Помилка пошуку (наприклад, контакту)
            return "Контакт не знайдено."
        except IndexError:
            # Помилка, коли не вистачає аргументів
            return f"Недостатньо аргументів. {get_usage_from_doc(func)}"

    return inner