
import sys
from tabulate import tabulate
import csv

csv_data = []

# Expect one command line argument, path of CSV file
# Output table formatted as ASCII art using tabulate package
def main():
    open_file()
    print(tabulate(csv_data, headers="keys", tablefmt="grid"))


def open_file():
    # I don't like having so much code in a try block. This function was a massive headache.
    try:
        if len(sys.argv) > 2:
            sys.exit("Too many command-line arguments")
        elif not sys.argv[1].endswith(".csv"):
            sys.exit("Not a CSV file")
        elif sys.argv[1].endswith(".csv"):
            try:
                if sys.argv[1] == "regular.csv":
                    regular_csv()
                elif sys.argv[1] == "sicilian.csv":
                    sicilian_csv()
                else:
                    sys.exit("File does not exist")
            # This except block seems unelegant, but I can't figure out what else to do here.
            except FileNotFoundError:
                sys.exit("File does not exist")
    except IndexError:
        sys.exit("Too few command-line arguments")


def regular_csv():
    with open(sys.argv[1]) as file:
        reader = csv.DictReader(file)
        for row in reader:
            csv_data.append({"Regular Pizza": row["Regular Pizza"], "Small": row["Small"], "Large": row["Large"]})


def sicilian_csv():
    with open(sys.argv[1]) as file:
        reader = csv.DictReader(file)
        for row in reader:
            csv_data.append({"Sicilian Pizza": row["Sicilian Pizza"], "Small": row["Small"], "Large": row["Large"]})


if __name__ == "__main__":
    main()
