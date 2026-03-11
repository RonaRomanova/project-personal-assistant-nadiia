def parse_input(user_input: str) -> tuple[str, list[str]]:
    """
    Розбирає введений рядок на команду та аргументи.
    """
    parts = user_input.split()

    if not parts:
        return "", []

    cmd, *args = parts
    return cmd.strip().lower(), args