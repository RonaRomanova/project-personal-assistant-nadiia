def input_error(func):
    """
    Декоратор для обробки помилок введення користувача.
    """

    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as error:
            return str(error)
        except KeyError:
            return "Контакт не знайдено."
        except IndexError:
            return "Введіть необхідні аргументи для команди."

    return inner