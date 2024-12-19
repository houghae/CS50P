import random

# Prompts the user for a level, n. If the user does not input a positive integer, the program should prompt again.
while True:
    try:
        level = int(input("Level: "))
        if level >= 1:
            break
        else:
            pass
    except ValueError:
        pass
    except NameError:
        pass

# Randomly generate an integer between 1 and n, inclusive, using the random module.
gameInt = random.randint(1, level)

# Prompts the user to guess that integer. If the guess is not a positive integer, the program should prompt the user again.
guess = None

while True:
    try:
        guess = int(input("Guess: "))
    except ValueError:
        pass
    if guess is not None and guess >=1:
        # If the guess is smaller than that integer, the program should output Too small! and prompt the user again.
        if guess < gameInt:
            print("Too small!")
            pass
        # If the guess is larger than that integer, the program should output Too large! and prompt the user again.
        elif guess > gameInt:
            print("Too large!")
            pass
        # If the guess is the same as that integer, the program should output Just right! and exit.
        elif guess == gameInt:
            break
        else:
            pass

print("Just right!")






