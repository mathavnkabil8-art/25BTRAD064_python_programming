# Accept temperature in Celsius from the user
celsius = float(input("Enter temperature in Celsius: "))

# Convert Celsius to Fahrenheit using the specified formula
fahrenheit = (celsius * 9 / 5) + 32

# Display the result using an f-string with two decimal places
print(f"{celsius:.2f}°C is equal to {fahrenheit:.2f}°F")
