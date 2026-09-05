# Recursive function to find the nth Fibonacci number
def fibonacci(n):
    # Base cases: the 1st term is 0, the 2nd term is 1
    if n == 0:
        return 0
    elif n == 1:
        return 1
    # Recursive case: add the two previous terms together
    else:
        return fibonacci(n - 1) + fibonacci(n - 2)


# --- Main Program ---
# Take input from the user for how many terms they want
terms = int(input("How many terms of the Fibonacci series do you want? "))

if terms <= 0:
    print("Please enter a positive integer.")
else:
    print("Fibonacci series:")
    # Loop to print each term one by one
    for i in range(terms):
        print(fibonacci(i), end=" ")
    print()  # Just for a clean new line at the end
