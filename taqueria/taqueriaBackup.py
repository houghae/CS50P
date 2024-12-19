menu = {
    "Baja Taco": 4.25,
    "Burrito": 7.50,
    "Bowl": 8.50,
    "Nachos": 11.00,
    "Quesadilla": 8.50,
    "Super Burrito": 8.50,
    "Super Quesadilla": 9.50,
    "Taco": 3.00,
    "Tortilla Salad": 8.00
}

def main():
    print("Use CTRL-D to end")
    while True:
        # Prompt user for menu item
        menuItem = input("Watcha havin'? ").title()
        try:
            x = matchItem(menuItem)
        # Ignore input not on menu
        except (KeyError, TypeError):
            pass
        else:
            print(x)


# Output running total expressed as $x.xx after each entry.
def matchItem(i):
    price = 0
    price += menu.get(i)
    return "$" + str(f"{price:.2f}")


try:
    while True:
        main()
# End ordering loop when user inputs ctrl-D.
except EOFError:
    pass
    print()


