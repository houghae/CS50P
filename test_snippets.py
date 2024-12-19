# “… vanity plates may contain a maximum of 6 characters (letters or numbers) and a minimum of 2 characters.”
def min_max(s):
    if 2 <= len(s) <= 6:
        print("True")
    else:
        print("False")

min_max(input("INPUT: "))
