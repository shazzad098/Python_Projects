import random

def main():
    print("\nWelcome to the Number Guessing Game!")
    secret_number = random.randint(1, 100)
    attempts = 0

    print("I'm thinking of a number between 1 and 100.")

    while True:
        guess = int(input("Enter your guess: "))
        attempts += 1

        if guess < secret_number:
            print("Too low! Try again.")
        elif guess > secret_number:
            print("Too high! Try again.")
        elif guess == secret_number:
            print(f"\n ** Congratulations! You guessed the number in {attempts} attempts! **")
            break
        else:
            print("Invalid input. Please enter a valid number.")

if __name__ == "__main__":
    main()