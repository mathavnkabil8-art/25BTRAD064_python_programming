import random


def number_guessing_game():
    print("====================================")
    print("   🎯 WELCOME TO THE GUESSING GAME!  ")
    print("====================================")
    print("I'm thinking of a number between 1 and 100.")

    # Generate a random number between 1 and 100
    secret_number = random.randint(1, 100)
    attempts = 0

    while True:
        try:
            # Ask the user for their guess
            guess = int(input("\nEnter your guess: "))
            attempts += 1

            # Check the user's guess against the secret number
            if guess < 1 or guess > 100:
                print("⚠️ Please guess a number within the 1 to 100 range.")
            elif guess < secret_number:
                print("📉 Too low! Try a higher number.")
            elif guess > secret_number:
                print("📈 Too high! Try a lower number.")
            else:
                print(f"\n🎉 CONGRATULATIONS! You found the number!")
                print(f"🏆 It took you {attempts} attempts to win.")
                break

        except ValueError:
            # Handle cases where the input is not a valid integer
            print("❌ Invalid input! Please enter a valid whole number.")


# Run the game
if __name__ == "__main__":
    number_guessing_game()
