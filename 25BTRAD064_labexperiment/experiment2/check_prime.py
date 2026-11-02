# Take user input
number = int(input("Enter a whole number to check: "))

# Numbers less than or equal to 1 are not prime
if number <= 1:
    print(number, "is NOT a prime number.")
else:
    is_prime = True
    i = 2

    # Loop from 2 up to the number - 1
    while i < number:
        if number % i == 0:
            is_prime = False  # Found a factor!
        i += 1

    # Output the final result
    if is_prime == True:
        print(number, "is a PRIME number!")
    else:
        print(number, "is NOT a prime number.")
