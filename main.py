import re

## Читаем адресную книгу в формате CSV в список contacts_list:
import csv

with open("phonebook_raw.csv", encoding='utf-8') as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)

## 1. Выполните пункты 1-3 задания.
## Ваш код

# Упорядочиваем данные
count = 0
for contact in contacts_list:
    pattern = re.compile(
        "([а-яёЁА-Я]+)[\s,]?([а-яёЁА-Я]+)[\s,]*([а-яёЁА-Я]+)?[,]*([а-яёЁА-Я]+)?[,]*([cа-яёЁА-Я\s–]+)?[,]*((\+7|8)\s?[(]?(\d{3})[)]?[-\s]?(\d{3})[-]?(\d{2})[-]?(\d{2})[\s]?[(]?(доб\.)?\s?(\d{4})?[)]?)?[\,]*([0-9a-zA-Z\.]+[@]{1}[a-zA-Z]+[\.]{1}[a-zA-Z]{2,3})?")
    pattern_repl = r"\1,\2,\3,\4,\5,\6,\14"
    text = ','.join(contact)
    result = re.sub(pattern, pattern_repl, text)
    contacts_list[count] = result.split(',')
    count += 1

# Получаем повторяющиеся фамилии и записываем их в сет doubles
doubles = set()
lastnames = []
for contact in contacts_list:
    lastnames.append(contact[0])

    for lastname in lastnames:
        if lastnames.count(lastname) >= 2:
            doubles.add(lastname)

# Помещаем всю информацию о повторяющихся контактах в отдельный массив double_contacts
# Дублеры будут идти друг за другом, т.е. первые 2 - один контакт, следующие 2 - другой контакт.
double_contacts = []
for double in doubles:
    for contact in contacts_list:
        if double in contact:
            double_contacts.append(contact)

# Создаем новый список без дубликатов
contacts_list_new = contacts_list
for double_contact in double_contacts:
    for contact in contacts_list_new:
        if double_contact[0] == contact[0]:
            contacts_list_new.remove(contact)

# Соединяем дубликаты и добавляем их в новый список
for index in range(0, len(double_contacts), 2):
    full_contact = ['', '', '', '', '', '', '']
    contact_1 = double_contacts[index]
    contact_2 = double_contacts[index + 1]

    for i in range(0, 10):
        try:
            if contact_1[i] != '':
                full_contact[i] = contact_1[i]
            else:
                full_contact[i] = contact_2[i]
        except Exception:
            continue
    contacts_list_new.append(full_contact)

# Приводим в порядок номера телефонов
count = 0
for contact in contacts_list_new:
    pattern = re.compile("(\+7|8)\s?[(]?(\d{3})[)]?[-\s]?(\d{3})[-]?(\d{2})[-]?(\d{2})[\s]?[(]?(доб\.)?\s?(\d{4})?[)]?")
    pattern_repl = r"+7(\2)\3-\4-\5 \6\7"
    result = re.sub(pattern, pattern_repl, contact[5])
    contacts_list_new[count][5] = result.strip()
    count += 1

## 2. Сохраните получившиеся данные в другой файл.
## Код для записи файла в формате CSV:
with open("phonebook.csv", "w", encoding="utf-8") as f:
    datawriter = csv.writer(f, delimiter=',')

    ## Вместо contacts_list подставьте свой список:
    datawriter.writerows(contacts_list_new)
