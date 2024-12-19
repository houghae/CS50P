import csv
import sys
name_house_list = []
first_last_house_list = []

def main():
    error_handling()


#This is much sexier than the previous program, pizza.py. I Like this error handling.
def error_handling():
    #Expect two command line arguments
    if len(sys.argv) < 3:
        sys.exit("Too few command-line arguments")
    elif len(sys.argv) > 3:
        sys.exit("Too many command-line arguments")
    else:
        try:
            csv_conversion()
        #First argument can't be read
        except FileNotFoundError:
            sys.exit(f"Could not read {sys.argv[1]}")


#Converts that input to that output, splitting each name into a first name and last name. Assume that each student will have both a first name and last name
#the name of an existing CSV file to read as input, whose columns are assumed to be, in order, name and house
#the name of a new CSV to write as output, whose columns should be, in order, first, last, and house
def csv_conversion():
    read_csv()
    append_dict()
    write_new_csv()


#DONE
def read_csv():
    #open argv1 as DictReader. Read out to a list.
    with open(sys.argv[1]) as file:
        reader = csv.DictReader(file)
        for row in reader:
            name_house_list.append({"name": row["name"], "house": row["house"]})

#DONE
def append_dict():
    #Append a dict to have first, last, house. Use split
    for name in name_house_list:
        last, first = name["name"].split(",")
        #Create new dict with three vars
        flh_dict = {"first": first.strip(), "last": last.strip(), "house": name["house"]}
        first_last_house_list.append(flh_dict)


def write_new_csv():
    #write out that dict using DictWriter to argv2
    with open(sys.argv[2], "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["first", "last", "house"])
        writer.writeheader()
        for name in first_last_house_list:
            writer.writerow(name)
        #writer.writerow({"first": first_last_house_list, "last": first_last_house_list, "house": first_last_house_list})
        #Take note, I originally tried to write the whole list to one row in the file. That was stupid.
        #In order to get rows and columns, you must iterate over each row with one dict at a time. Smart.


if __name__ == "__main__":
    main()
