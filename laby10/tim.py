import psycopg2
import csv

# -------------------
# CONNECTION
# -------------------
conn = psycopg2.connect(
    dbname="phonebook",
    user="postgres",
    password="moiponos228",
    host="localhost",
    port="5432"
)

cursor = conn.cursor()


# -------------------
# CREATE
# -------------------
def add_contact(name, phone):
    cursor.execute(
        "INSERT INTO phonebook (name, phone) VALUES (%s, %s)",
        (name, phone)
    )
    conn.commit()
    print("Added:", name)


# -------------------
# READ
# -------------------
def show_all():
    cursor.execute("SELECT * FROM phonebook")
    rows = cursor.fetchall()
    for row in rows:
        print(row)


def find_by_name(name):
    cursor.execute("SELECT * FROM phonebook WHERE name ILIKE %s", (f"%{name}%",))
    rows = cursor.fetchall()
    for row in rows:
        print(row)


def find_by_phone(phone):
    cursor.execute("SELECT * FROM phonebook WHERE phone=%s", (phone,))
    rows = cursor.fetchall()
    for row in rows:
        print(row)


# -------------------
# UPDATE
# -------------------
def update_name(old_name, new_name):
    cursor.execute(
        "UPDATE phonebook SET name=%s WHERE name=%s",
        (new_name, old_name)
    )
    conn.commit()
    print("Updated name:", old_name, "→", new_name)


def update_phone(name, new_phone):
    cursor.execute(
        "UPDATE phonebook SET phone=%s WHERE name=%s",
        (new_phone, name)
    )
    conn.commit()
    print("Updated phone for", name)


# -------------------
# DELETE
# -------------------
def delete_by_name(name):
    cursor.execute("DELETE FROM phonebook WHERE name=%s", (name,))
    conn.commit()
    print("Deleted:", name)


def delete_by_phone(phone):
    cursor.execute("DELETE FROM phonebook WHERE phone=%s", (phone,))
    conn.commit()
    print("Deleted:", phone)


# -------------------
# CSV IMPORT
# -------------------
def upload_csv(path):
    with open(path, encoding="utf-8") as f:
        reader = csv.reader(f)
        for name, phone in reader:
            cursor.execute(
                "INSERT INTO phonebook (name, phone) VALUES (%s, %s)",
                (name, phone)
            )
    conn.commit()
    print("CSV uploaded.")


# -------------------
# MENU
# -------------------
def menu():
    while True:
        print("\nPhoneBook Menu:")
        print("1. Add contact")
        print("2. Show all contacts")
        print("3. Find by name")
        print("4. Find by phone")
        print("5. Update name")
        print("6. Update phone")
        print("7. Delete by name")
        print("8. Delete by phone")
        print("9. Upload CSV")
        print("0. Exit")

        choice = input(">>> ")

        if choice == "1":
            name = input("Name: ")
            phone = input("Phone: ")
            add_contact(name, phone)

        elif choice == "2":
            show_all()

        elif choice == "3":
            n = input("Search name: ")
            find_by_name(n)

        elif choice == "4":
            p = input("Search phone: ")
            find_by_phone(p)

        elif choice == "5":
            old = input("Old name: ")
            new = input("New name: ")
            update_name(old, new)

        elif choice == "6":
            name = input("Name: ")
            new_phone = input("New phone: ")
            update_phone(name, new_phone)

        elif choice == "7":
            n = input("Delete name: ")
            delete_by_name(n)

        elif choice == "8":
            p = input("Delete phone: ")
            delete_by_phone(p)

        elif choice == "9":
            path = input("CSV path: ")
            upload_csv(path)

        elif choice == "0":
            print("Goodbye!")
            break


if __name__ == "__main__":
    menu()
