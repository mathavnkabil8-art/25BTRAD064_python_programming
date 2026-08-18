# 1. INPUT: Get two numbers from the user
num1 = float(input("Enter first number: "))
num2 = float(input("Enter second number: "))
# 2. OPERATORS & VARIABLES: Perform basic calculations
addition = num1 + num2
subtraction = num1 - num2
multiplication = num1 * num2

division = num1 / num2
# 3. OUTPUT: Display all results
print("\n--- CALCULATOR RESULTS ---")
print("Addition (+):", addition)
print("Subtraction (-):", subtraction)
print("Multiplication (*):", multiplication)
print("Division (/):", division)

# 1. INPUT: Get dimensions from the user
length = float(input("Enter rectangle length: "))
width = float(input("Enter rectangle width: "))
radius = float(input("Enter circle radius: "))
# 2. OPERATORS: Calculate the areas using math formulas
rectangle_area = length * width
circle_area = 3.14 * radius * radius

# 3. OUTPUT: Display the calculated results
print("\n--- AREA RESULTS ---")
print("Rectangle Area:", rectangle_area)
print("Circle Area:", circle_area)
