from collections import UserDict
import re


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value):
        if not re.fullmatch(r'\d{10}', value):
            raise ValueError("Invalid phone number. Must be 10 digits.")
        super().__init__(value)


class Record:
    def __init__(self, name_value, phones=None):
        self.name = Name(name_value)
        self.phones = phones if phones is not None else []

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        phone_to_remove = self.find_phone(phone)
        if phone_to_remove:
            self.phones.remove(phone_to_remove)

    def edit_phone(self, old_phone, new_phone):
        phone_to_edit = self.find_phone(old_phone)
        if phone_to_edit:
            phone_to_edit.value = new_phone

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"


class AddressBook(UserDict):
    def add_record(self, record_inf):
        self.data[record_inf.name.value] = record_inf

    def find(self, name_key):
        return self.data.get(name_key)

    def delete(self, name_key):
        if name_key in self.data:
            del self.data[name_key]


book = AddressBook()

john_record = Record("John")
john_record.add_phone("1234567890")
john_record.add_phone("5555555555")

book.add_record(john_record)

jane_record = Record("Jane")
jane_record.add_phone("9876543210")
book.add_record(jane_record)

for record_name, record in book.data.items():
    print(record)

john = book.find("John")
if john:
    john.edit_phone("1234567890", "1112223333")
    print(john)

found_phone = john.find_phone("5555555555") if john else None
if found_phone:
    print(f"{john.name}: {found_phone}")

book.delete("Jane")
