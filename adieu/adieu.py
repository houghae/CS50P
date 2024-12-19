import inflect

p = inflect.engine()
nameList = []

# prompts the user for names, one per line, until the user inputs control-d
try:
    while True:
        namePrompt = input("Name: ")
        nameList.append(namePrompt)
except EOFError:
    pass

# Use inflect to join words into a list
nameList = p.join(nameList)
print("Adieu, adieu, to", nameList)
