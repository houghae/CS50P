import re

# Implement a function called validate that expects an IPv4 address as input as a str and then returns True or False if it's valid or not.
# IPv4 is #.#.#.# wherein # is 0-255.
# Structure numb3rs.py as follows, but you may not import any other libraries.
# 0-255. 0, 1-9, 10-99, 100-199, 200-249, 250-255

def main():
    print(validate(input("IPv4 Address: ")))


def validate(ip):
    if re.search(r"^((25[0-5])|(2[0-4][0-9])|(1[0-9][0-9])|([1-9][0-9])|[1-9]|0)\.((25[0-5])|(2[0-4][0-9])|(1[0-9][0-9])|([1-9][0-9])|[1-9]|0)\.((25[0-5])|(2[0-4][0-9])|(1[0-9][0-9])|([1-9][0-9])|[1-9]|0)\.((25[0-5])|(2[0-4][0-9])|(1[0-9][0-9])|([1-9][0-9])|[1-9]|0)$", ip):
        return True
    else:
        return False


if __name__ == "__main__":
    main()
