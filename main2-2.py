from collections import UserDict


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value):
        if len(value) == 10 and value.isdigit():
            super().__init__(value)
        else:
            raise ValueError("Phone number must be 10 digits")


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        phone_to_remove = Phone(phone)
        for p in self.phones:
            if p.value == phone_to_remove.value:
                self.phones.remove(p)
                return

    def edit_phone(self, old_phone, new_phone):
        for idx, phone in enumerate(self.phones):
            if phone.value == old_phone:
                self.phones[idx] = Phone(new_phone)
                return

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def __str__(self):
        return f"Contact name: {self.name}, phones: {'; '.join(str(p) for p in self.phones)}"


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]


def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, args


def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "add":
            try:
                record = Record(args[0])
                record.add_phone(args[1])
                book.add_record(record)
                print(f"Contact {args[0]} added.")
            except IndexError:
                print("Invalid format. Use: add [name] [phone]")

        elif command == "change":
            try:
                record = book.find(args[0])
                if record:
                    record.edit_phone(args[1], args[2])
                    print(f"Phone for {args[0]} changed.")
                else:
                    print("Contact not found.")
            except IndexError:
                print("Invalid format. Use: change [name] [old phone] [new phone]")

        elif command == "phone":
            try:
                record = book.find(args[0])
                if record:
                    print(f"Phones for {args[0]}: {', '.join(p.value for p in record.phones)}")
                else:
                    print("Contact not found.")
            except IndexError:
                print("Invalid format. Use: phone [name]")

        elif command == "all":
            for name, record in book.data.items():
                print(record)

        elif command == "remove":
            try:
                book.delete(args[0])
                print(f"Contact {args[0]} removed.")
            except IndexError:
                print("Invalid format. Use: remove [name]")

        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
