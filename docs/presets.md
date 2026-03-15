# CLI Command Presets

Use these examples to quickly interact with the Personal Assistant. You can copy and paste these into the prompt.

## 👤 Contacts Management

### Add or Update Contact
```bash
# Базовий приклад
add-contact "Nadiia Romanova" 0931234567

# Додавання з усіма полями та декількома номерами
add-contact "Elon Musk" 0991234999 380991234998 email=elon@spacex.com birthday=28.06.1971 address="Mars, Base 1"

# Українські імена та адреси в лапках
add-contact "Іван Іваненко" 0971234567 address="вул. Хрещатик, 1, Київ"

# Додавання тільки email або тільки адреси вже існуючому контакту
add-contact "Elon Musk" email=elon@x.com
add-contact "Elon Musk" address="Starbase, Texas"
```

### Edit Contact Details
```bash
# Зміна старого номера на новий (+380 формат також підтримується)
edit-phone "Nadiia Romanova" 0931234567 0937654321
edit-phone "Elon Musk" +380991234999 +380991234992

# Зміна електронної пошти
edit-email "Elon Musk" elon@spacex.com elon@x.com

# Установка або оновлення дня народження
edit-birthday "Elon Musk" 28.06.1971

# Оновлення фізичної адреси
edit-address "Elon Musk" "Boca Chica, Texas"
```

### Search and List
```bash
# Показати всі контакти
all-contacts

# Пошук за ім'ям (частина імені)
find-contact "Nadiia"

# Складний пошук за декількома полями
find-contact "Elon" phone=099
find-contact email=example.com

# Список іменинників на наступні 7 днів
birthdays
```

### Delete Contact
```bash
delete-contact "Nadiia Romanova"
```

## 📝 Notes Management

### Add Note
```bash
# Нотатка без тегів
add-note "Забрати посилку о 18:00"

# Нотатка з декількома тегами
add-note "Купити подарунок на день народження" #важливо #плани #сім'я

# Робочі нотатки
add-note "Підготувати звіт до понеділка" #work #deadline #urgent
add-note "Review the project-personal-assistant code" #work #python
```

### Edit Note
```bash
# Редагування тексту за ID (ID можна побачити в all-notes)
edit-note 1 "Забрати посилку о 19:00 (перенесли)"

# Робота з тегами (додавання та видалення)
edit-tag 1 add терміново
edit-tag 1 add важливо
edit-tag 1 delete плани
```

### Search and List Notes
```bash
# Список усіх нотаток з їхніми ID
all-notes

# Пошук за текстом
find-note "подарунок"

# Пошук за конкретним тегом
find-note #work
find-note #терміново
```

### Delete Note
```bash
# Видалення за ID
delete-note 1
```

## ⚙️ System Commands
```bash
# Привітання
hello

# Показати меню допомоги
help

# Вихід (можна також використовувати 'close' або Ctrl+C)
exit
```
