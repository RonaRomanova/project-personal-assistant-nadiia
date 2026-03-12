from datetime import datetime

def parse_date(value: str) -> str | None:
    """
    Перетворює рядок дати з поширених форматів у формат YYYY-MM-DD.
    Підтримувані формати: DD.MM.YYYY, YYYY-MM-DD, DD/MM/YYYY, MM/DD/YYYY.
    Повертає нормалізований рядок або None, якщо жоден формат не підійшов.
    """
    for fmt in ("%d.%m.%Y", "%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y"):
        try:
            dt = datetime.strptime(value, fmt)
            return dt.strftime("%Y-%m-%d")
        except ValueError:
            continue
    return None
