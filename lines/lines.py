import sys


# Expects one command line argument, outputs number of lines of code
# Exclude comments, blank lines
# Enact sys exit if not exactly one argument, file name doesn't end in .py, or file doesn't exist
def main():
    all_lines = open_file()
    scrub_lines = loc_scrub(all_lines)
# Print len of list
    print(len(scrub_lines))


def open_file():
    try:
        # if file ends in .py and argv == 1
        if len(sys.argv) > 2:
            sys.exit("Too many command-line arguments")
        elif not sys.argv[1].endswith(".py"):
            sys.exit("Not a Python file")
        else:
            try:
                # Open file from sys.argv[1]
                with open(sys.argv[1]) as file:
                    return file.readlines()
            # except file not found error
            except FileNotFoundError:
                sys.exit("File does not exist")
    except IndexError:
        sys.exit("Too few command-line arguments")


def loc_scrub(loc):
    line_list = []
    # Remove blank lines and comments by using rstrip, remove #, ""
    for line in loc:
        line = line.strip()
        if not line.startswith("#") and line != "":
            line_list.append(line)
    return line_list


if __name__ == "__main__":
    main()
