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
    currentCost = 0
    while True:
        # Prompt user for menu item
        menuItem = input("Watcha havin'? ").title()
        if menuItem in menu:
            try:
                price = menu.get(menuItem)
            # Ignore input not on menu
            except (KeyError, TypeError):
                pass
            # Output running total expressed as $x.xx after each entry.
            else:
                currentCost += price
                print("$" + str(f"{currentCost:.2f}"))


try:
    while True:
        main()
# End ordering loop when user inputs ctrl-D.
except EOFError:
    pass
    print()


