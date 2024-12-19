# This problem was SUCH A HEADACHE!


# Define variable for punctuation

def main():
    plate = input("Plate: ")
    if is_valid(plate):
        print("Valid")
    else:
        print("Invalid")

def is_valid(s):
    if first_two_char(s) and min_max(s) and end_with_numbers(s) and no_punctuation(s):
        return True
    return False

# “All vanity plates must start with at least two letters.”
def first_two_char(s):
    return s[:2].isalpha()

# “… vanity plates may contain a maximum of 6 characters (letters or numbers) and a minimum of 2 characters.”
def min_max(s):
    return 2 <= len(s) <= 6

# “Numbers cannot be used in the middle of a plate; they must come at the end. The first number used cannot be a ‘0’.”
# This function took forever to figure out. Line 36 in particular. Revisit these concepts.
# First, iterate through string until finding a number. If number is 0, then invalid.
    # Next, if nonzero number found, confirm no letters come after it.
def end_with_numbers(s):
    i = 0
    while i < len(s):
        if s[i].isalpha() == False:
            if s[i] == "0":
                return False
            if s[i].isdigit() and any(char.isalpha() for char in s[i+1:]):
                return False
            else:
                break
        i += 1
    return True

# “No periods, spaces, or punctuation marks are allowed.”
def no_punctuation(s):
    return all(i.isalpha() or i.isdigit() for i in s)


main()
