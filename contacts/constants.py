"""
Centralized constants for the contacts module.
"""

# Regex patterns
PHONE_REGEX = r"[^\d\+]" # only digits and plus sign
DIGITS_ONLY_REGEX = r"\D"
EMAIL_REGEX = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

# Format strings
DATE_FORMAT = "%Y-%m-%d"
UKRAINIAN_DATE_FORMAT = "%d.%m.%Y"

# Phone validation constants
UKRAINE_COUNTRY_CODE = "380"
MIN_PHONE_DIGITS = 9
MAX_PHONE_DIGITS = 12
NORMALIZED_PHONE_LENGTH = 13

# Default display values
NOT_SPECIFIED = "не вказано"
NO_NOTES = "📝 Нотаток немає."
CONTACT_NOT_FOUND = "Контакт не знайдено."
NOTE_NOT_FOUND = "Нотатку не знайдено."

# Table configurations
TABLE_NAME_MAX_WIDTH = 15
TABLE_PHONE_MAX_WIDTH = 28
TABLE_EMAIL_MAX_WIDTH = 40
TABLE_ADDRESS_MAX_WIDTH = 40
TABLE_NOTE_MAX_WIDTH = 50
TABLE_UPCOMING_NAME_MAX_WIDTH = 20
