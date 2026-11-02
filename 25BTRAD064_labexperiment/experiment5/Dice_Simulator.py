import random 
def roll_dice(number_of_dice):
    results = []
    for _ in range(number_of_dice):
        results.append(random.randint(1, 6))
    return results
 
 
def main():
    try:
        number_of_dice = int(input("How many dice do you want to roll? "))
        number_of_rolls = int(input("How many times do you want to roll them? "))
 
        if number_of_dice <= 0 or number_of_rolls <= 0:
            print("Please enter positive integers.")
            return
 
        frequency = {face: 0 for face in range(1, 7)}
        for roll_number in range(1, number_of_rolls + 1):
            results = roll_dice(number_of_dice)
            print(f"Roll {roll_number}: {results}")
            for result in results:
                frequency[result] += 1
 
        print("Frequency of each face:")
        for face, count in frequency.items():
            print(f"{face}: {count}")
 
    except ValueError:
        print("Invalid input. Please enter whole numbers.")
 
 
if __name__ == "__main__":
    main()
