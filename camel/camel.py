# Get user input in camel case.
file_name = input("'Tis thou file name? ")

# Iterate through each letter in the input, finding uppercase and adding an underscore
for iterable in file_name:
    if iterable.islower():
        print (iterable, end="")
    elif iterable.isupper():
        print("_" + iterable.lower(), end="")

# add a line so command prompt is a line below the answer
print("")
