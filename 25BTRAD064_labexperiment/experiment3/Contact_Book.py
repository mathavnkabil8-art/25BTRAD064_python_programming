contacts = {}
 
def add_contact():
    name = input("Enter contact name: ").strip().title()
    if not name:
        print("Name cannot be empty.")
        return
    phone = input("Enter phone number: ").strip()
    email = input("Enter email address: ").strip()
    contacts[name] = {"phone": phone, "email": email}
    print("Contact added successfully.")
 
def search_contact():
    name = input("Enter the name to search: ").strip().title()
    if name in contacts:
        print("Name:", name)
        print("Phone:", contacts[name]["phone"])
        print("Email:", contacts[name]["email"])
    else:
        print("Contact not found.")
 
def update_contact():
    name = input("Enter the name to update: ").strip().title()
    if name not in contacts:
        print("Contact not found.")
        return
    phone = input("Enter new phone number: ").strip()
    email = input("Enter new email address: ").strip()
    contacts[name] = {"phone": phone, "email": email}
    print("Contact updated successfully.")
 
def delete_contact():
    name = input("Enter the name to delete: ").strip().title()
    if name in contacts:
        del contacts[name]
        print("Contact deleted successfully.")
    else:
        print("Contact not found.")
 
def display_contacts():
    if not contacts:
        print("Contact book is empty.")
        return
    print("\n--- Contact Book ---")
    for name, details in sorted(contacts.items()):
        print(f"Name: {name} | Phone: {details['phone']} | Email: {details['email']}")
 
while True:
    print("\n1. Add contact")
    print("2. Search contact")
    print("3. Update contact")
    print("4. Delete contact")
    print("5. Display all contacts")
    print("6. Exit")
    choice = input("Choose an option (1-6): ").strip()
 
    if choice == "1":
        add_contact()
    elif choice == "2":
        search_contact()
    elif choice == "3":
        update_contact()
    elif choice == "4":
        delete_contact()
    elif choice == "5":
        display_contacts()
    elif choice == "6":
        print("Exiting contact book.")
        break
    else:
        print("Invalid choice. Please choose from 1 to 6.")
