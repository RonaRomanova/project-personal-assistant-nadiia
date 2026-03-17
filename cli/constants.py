"""
Constants for UI and command handling.
"""

HELP_TEXT = (
    "\n[bold underline magenta]🌟 ПЕРСОНАЛЬНИЙ ПОМІЧНИК: ПОВНЕ КЕРІВНИЦТВО 🌟[/bold underline magenta]\n\n"
    "[dim italic]Позначення: <обов'язковий>, \\[необов'язковий][/dim italic]\n\n"
    
    "[bold cyan]👤 КОНТАКТИ[/bold cyan]\n"
    "  [green]• add-contact[/green] - [i]Створення або оновлення контакту.[/i]\n"
    "    [dim]Формат:[/dim] [white]add-contact <Ім'я> \\[тел1 тел2 ...] \\[email=...] \\[address=...] \\[birthday=...][/white]\n"
    "    [dim]Приклад:[/dim] [yellow]add-contact 'Elon Musk' 0991234999 email=elon@musk.com[/yellow]\n\n"
    
    "  [green]• edit-phone[/green] - [i]Зміна номера телефону.[/i]\n"
    "    [dim]Формат:[/dim] [white]edit-phone <Ім'я> <старий_тел> <новий_тел>[/white]\n"
    "    [dim]Приклад:[/dim] [yellow]edit-phone 'Elon Musk' +380991234999 +380991234998[/yellow]\n\n"
    
    "  [green]• edit-email[/green] - [i]Зміна електронної пошти.[/i]\n"
    "    [dim]Формат:[/dim] [white]edit-email <Ім'я> <старий_email> <новий_email>[/white]\n"
    "    [dim]Приклад:[/dim] [yellow]edit-email 'Elon Musk' old@mail.com new@mail.com[/yellow]\n\n"
    
    "  [green]• edit-address[/green] - [i]Оновлення фізичної адреси.[/i]\n"
    "    [dim]Формат:[/dim] [white]edit-address <Ім'я> <нова_адреса>[/white]\n"
    "    [dim]Приклад:[/dim] [yellow]edit-address 'Elon Musk' 'Mars, Base 1'[/yellow]\n\n"
    
    "  [green]• edit-birthday[/green] - [i]Установка або зміна дня народження.[/i]\n"
    "    [dim]Формат:[/dim] [white]edit-birthday <Ім'я> <ДД.ММ.РРРР>[/white]\n"
    "    [dim]Приклад:[/dim] [yellow]edit-birthday 'Elon Musk' 28.06.1971[/yellow]\n\n"
    
    "  [green]• all-contacts[/green] - [i]Відображення всіх контактів.[/i]\n"
    "    [dim]Формат:[/dim] [white]all-contacts[/white]\n\n"
    
    "  [green]• find-contact[/green] - [i]Повнотекстовий пошук за будь-яким полем або за ключами.[/i]\n"
    "    [dim]Формат:[/dim] [white]find-contact <запит> \\[phone=...] \\[email=...] \\[address=...] \\[birthday=...][/white]\n"
    "    [dim]Приклад:[/dim] [yellow]find-contact 'Elon'[/yellow]\n\n"
    
    "  [green]• birthdays[/green] - [i]Іменинники на найближчі 7 днів.[/i]\n"
    "    [dim]Формат:[/dim] [white]birthdays[/white]\n\n"
    
    "  [green]• delete-contact[/green] - [i]Видалення контакту.[/i]\n"
    "    [dim]Формат:[/dim] [white]delete-contact <Ім'я>[/white]\n"
    "    [dim]Приклад:[/dim] [yellow]delete-contact 'Elon Musk'[/yellow]\n\n"
    
    "[bold cyan]📝 НОТАТКИ[/bold cyan]\n"
    "  [green]• add-note[/green] - [i]Створення нової нотатки.[/i]\n"
    "    [dim]Формат:[/dim] [white]add-note <\"текст\"> \\[тег1 тег2 ...][/white]\n"
    "    [dim]Приклад:[/dim] [yellow]add-note \"Купити Space-X\" акції важливо[/yellow]\n\n"
    
    "  [green]• edit-note[/green] - [i]Редагування тексту нотатки.[/i]\n"
    "    [dim]Формат:[/dim] [white]edit-note <ID> <\"новий текст\">[/white]\n"
    "    [dim]Приклад:[/dim] [yellow]edit-note 1 \"Полетіти на Марс\"[/yellow]\n\n"
    
    "  [green]• edit-tag[/green] - [i]Керування тегами нотатки.[/i]\n"
    "    [dim]Формат:[/dim] [white]edit-tag <ID> <add|delete> <тег>[/white]\n"
    "    [dim]Приклад:[/dim] [yellow]edit-tag 1 add терміново[/yellow]\n\n"
    
    "  [green]• find-note[/green] - [i]Пошук за змістом, тегом або ключами tag=, text=.[/i]\n"
    "    [dim]Формат:[/dim] [white]find-note <запит> \\[tag=...] \\[text=...][/white]\n"
    "    [dim]Приклад:[/dim] [yellow]find-note 'Марс' tag=важливо[/yellow]\n\n"
    
    "  [green]• all-notes[/green] - [i]Список усіх нотаток.[/i]\n"
    "    [dim]Формат:[/dim] [white]all-notes[/white]\n\n"
    
    "  [green]• delete-note[/green] - [i]Видалення нотатки за номером.[/i]\n"
    "    [dim]Формат:[/dim] [white]delete-note <ID>[/white]\n\n"
    
    "[bold cyan]⚙️ СИСТЕМА[/bold cyan]\n"
    "  [green]• hello[/green]          [dim]- Привітання від бота.[/dim]\n"
    "  [green]• help[/green]           [dim]- Це меню допомоги.[/dim]\n"
    "  [green]• close / exit[/green]  [dim]- Вихід зі збереженням даних.[/dim]\n"
)
WELCOME_MSG = (
    "Привіт. Я — Personal Assistant "
    "[bold magenta]NADIIA2[/bold magenta] 🦄!\n\n"
    "Я не зміню твоє життя за 3 секунди, "
    "не пообіцяю “AI magic” і не буду вдавати з себе "
    "🍎 [i cyan]iPhone 27 Pro Max[/i cyan].\n"
    "Я просто допоможу тобі з організацією "
    "твоїх контактів, введи 'help' щоб побачити "
    "всі доступні команди."
)
HOW_CAN_I_HELP="Як я можу вам допомогти?"
EXIT_MSG = "До побачення!"
HELP_PROMPT = "\n >>>>>> Введіть команду: "
UNKNOWN_COMMAND = "Невірна команда."
