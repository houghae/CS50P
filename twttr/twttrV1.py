# Make a file that outputs the user's input, but without vowels
# Build similar to camel case problem

# Define a list of vowels
vowels = ["a", "e", "i", "o", "u", "A", "E", "I", "O", "U"]

# Get user input
user_input = input("Input: ")
print("Output: ", end="")

# Iterate through each letter in the string. If vowel, remove it
for i in user_input:
    if i in vowels:
        i = i.replace(i, "")
        print(i, end="")
    else:
        print(i, end="")
print()


# Output new string without vowels
