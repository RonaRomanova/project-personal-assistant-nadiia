from datetime import datetime

from contacts.constants import DATE_FORMAT


def parse_date(value: str) -> str | None:
    """
    Перетворює рядок дати з поширених форматів у формат YYYY-MM-DD.
    Підтримувані формати: DD.MM.YYYY, YYYY-MM-DD, DD/MM/YYYY, MM/DD/YYYY.
    Повертає нормалізований рядок або None, якщо жоден формат не підійшов.
    """
    for fmt in ("%d.%m.%Y", DATE_FORMAT, "%d/%m/%Y", "%m/%d/%Y"):
        try:
            dt = datetime.strptime(value, fmt)
            return dt.strftime(DATE_FORMAT)
        except ValueError:
            continue
    return None


def print_ukrainian_flag(width=10, height=1, margin_top=1, margin_bottom=1):
    # ANSI color codes
    blue = "\033[48;2;0;87;183m"  # Deep Blue
    yellow = "\033[48;2;255;215;0m"  # Gold/Yellow
    reset = "\033[0m"

    for _ in range(margin_top):
        print("\r")

    # Print Blue Top
    for _ in range(height):
        print(f"{blue}{' ' * width}{reset}")

    # Print Yellow Bottom
    for _ in range(height):
        print(f"{yellow}{' ' * width}{reset}")

    for _ in range(margin_bottom):
        print("\r")
