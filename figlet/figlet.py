import random
import sys

from pyfiglet import Figlet
figlet = Figlet()

fontList = figlet.getFonts()
arguments = ["-f", "--font"]

# Expects zero or two command-line arguments:
# Zero if the user would like to output text in a random font
if len(sys.argv) < 2:
    randomFont = random.choice(fontList)
    figlet.setFont(font=randomFont)
    getInput = input("Input: ")
    print(figlet.renderText(getInput))

# Two if the user would like to output text in a specific font
    # the first of the two should be -f or --font
    # the second of the two should be the name of the font
elif len(sys.argv) == 3:
    if sys.argv[1] in arguments and sys.argv[2] in fontList:
        figlet.setFont(font = sys.argv[2])
        getInput = input("Input: ")
        print(figlet.renderText(getInput))
    else:
        sys.exit("Invalid usage")
else:
    sys.exit("Invalid usage")

# Prompts the user for a str of text.


# Outputs that text in the desired font.
