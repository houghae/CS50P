# Create an empty dict
groceryDict = {}

# one per line, until the user inputs control-d
while True:
    try:
        # prompts the user for items, convert to uppercase
        groceryItem = input().upper()
    except EOFError:
        break
    else:
        # Add input to dict. Input should be the key, number of times entered should be the value
        if groceryItem in groceryDict:
            groceryDict[groceryItem] += 1
        else:
            groceryDict[groceryItem] = 1

# Print dict sorted alphabetically by item,
# prefixing each line with the number of times the user inputted that item.
print()
for key in sorted(groceryDict):
    print(groceryDict[key], key)




