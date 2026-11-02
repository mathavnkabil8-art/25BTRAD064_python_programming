students = {}
 
def calculate_grade(mark):
    if mark >= 90:
        return "A+"
    elif mark >= 80:
        return "A"
    elif mark >= 70:
        return "B"
    elif mark >= 60:
        return "C"
    elif mark >= 50:
        return "D"
    else:
        return "F"
 
count = int(input("Enter the number of students: "))
 
for i in range(count):
    print(f"\nStudent {i + 1}")
    name = input("Enter student name: ").strip().title()
 
    try:
        mark = float(input("Enter marks (0-100): "))
        if mark < 0 or mark > 100:
            print("Marks must be between 0 and 100. Student skipped.")
            continue
    except ValueError:
        print("Invalid marks. Student skipped.")
        continue
 
    students[name] = {"marks": mark, "grade": calculate_grade(mark)}
 
print("\n--- Student Results ---")
if not students:
    print("No valid student records were entered.")
else:
    for name, result in students.items():
        print(f"Name: {name}, Marks: {result['marks']:.1f}, Grade: {result['grade']}")
