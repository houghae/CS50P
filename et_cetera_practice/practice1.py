import random

# Sets
def set_function():
    """
    Create function that produces a random set of numbers. Return the full list and the list set.
    """

    # Create a random list of numbers
        # Create an empty list
        # Call randomrange and store value in the list
        # Iterate random values over the list
    # Get the set of those numbers
    
    rand_list = []
    for _ in range(10):
        rand_num = random.randrange(10)
        rand_list.append(rand_num)
    
    rand_set = set(rand_list)
    return rand_list, rand_set


def set_adv():
    """
    Create list comp version of the set_function.
    """

    rand_list = [
        random.randrange(10) for _ in range(10)
    ]

    return rand_list, set(rand_list)

def set_practice():
    # Create a set directly with curly braces
    my_set = {1,2,3,4,5,6,6,6,4,7,8,9}
    return my_set



# Type hints
def meow(n):
    for _ in range(n):
        print("meow")

number = input("Number: ")
meow(number)










# Docstrings
# argparse
# Unpacking
# args, kwargs
# map
# List comprehensions
# filter
# Dictionary comprehensions
# enumerate
# Generators and iterators


def main():
#    print(*set_function(), sep="\n")
#    print(*set_adv(), sep="\n")
    print(set_practice())



if __name__=="__main__":
    main()