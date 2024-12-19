import random


def main():
    points = 0
    tries = 1
    level = get_level() # Get level from user
    for _ in range(10): # Loop for 10 distinct math equations
        x = generate_integer(level)
        y = generate_integer(level)
        z = x + y
        while True: # Create loop 3 times to answer the problem
            answer = input(str(x) + " + " + str(y) + " = ")
            try:
                answer = int(answer)
            except ValueError:
                pass
            if answer == z:
                points += 1
                break
            elif tries < 3:
                print("EEE")
                tries += 1
                pass
            else: # Provide answer after 3rd try
                print(x, "+", y, "=", z)
                break
    print("Score: ", points) # Output user's score, correct answers out of 10.


# Prompt user for level, return 1, 2, or 3.
def get_level():
    while True:
        try:
            userChoice = int(input("Level: "))
            if 1 <= userChoice <= 3:
                return userChoice
            elif userChoice < 1 or userChoice > 3:
                pass
        except ValueError:
            pass


# Return random non-negative integer with 'level' digits.
def generate_integer(level):
    if level == 1:
        randoVars = random.randint(0, 9)
        return randoVars
    elif level == 2:
        randoVars = random.randint(10, 99)
        return randoVars
    elif level == 3:
        randoVars = random.randint(100, 999)
        return randoVars


if __name__ == "__main__":
    main()
