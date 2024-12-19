# Instructions_____________________________________________________________________________________________________________________________
# Implement a function called count that expects a line of text as input as a str and returns, as an int,
# the number of times that “um” appears in that text, case-insensitively, as a word unto itself, not as a substring of some other word.
# For instance, given text like hello, um, world, the function should return 1. Given text like yummy, though, the function should return 0.

# Structure um.py as follows, wherein you’re welcome to modify main and/or implement other functions as you see fit,
# but you may not import any other libraries. You’re welcome, but not required, to use re and/or sys.
# Tips: re.findall, \b for finding the begining of a word.
#___________________________________________________________________________________________________________________________________________
# Note to self: This program went so fast. I think I spent more time on the pseudo code than the actual code. Troubleshooting yielded no problems.

import re


def main():
    print(count(input("Text: ")))


def count(s):
    return len(regex(s))


def regex(s):
    # regex function that finds all ums, assign to a list variable.
    return re.findall(r"\b[u|U][m|M]\b", s)


if __name__ == "__main__":
    main()
