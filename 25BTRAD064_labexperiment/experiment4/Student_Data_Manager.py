import json
import os
 
FILENAME = "students.json"
 
def load_students():
    if not os.path.exists(FILENAME):
        return {}
    try:
        with open(FILENAME, "r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError):
        return {}
 
def save_students(students):
    with open(FILENAME, "w", encoding="utf-8") as file:
        json.dump(students, file, indent=4)
 
def main():
    students = load_students()
 
    while True:
        print("\n1. Add/Update  2. Search  3. Display  4. Exit")
        choice = input("Enter choice: ").strip()
 
        if choice == "1":
            student_id = input("Enter student ID: ").strip()
            name = input("Enter student name: ").strip()
            if not student_id or not name:
                print("ID and name cannot be empty.")
                continue
            students[student_id] = {"name": name}
            save_students(students)
            print("Student record saved.")
 
        elif choice == "2":
            student_id = input("Enter student ID to search: ").strip()
            if student_id in students:
                print("Record:", student_id, students[student_id])
            else:
                print("Student not found.")
 
        elif choice == "3":
            if not students:
                print("No student records available.")
            else:
                for student_id, details in students.items():
                    print(student_id, "-", details["name"])
 
        elif choice == "4":
            print("Exiting Student Data Manager.")
            break
        else:
            print("Invalid choice. Please try again.")
 
if __name__ == "__main__":
    main()
