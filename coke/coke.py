print("50 cents for a Coke. Pay in 5, 10, or 25 cent denominations")
# Create variable to keep track of amount due
amount_due = 50
# Create loop until amount due is >=0
while amount_due > 0:
    # print amount due
    print("Amount Due:", amount_due)
    # get the amount
    user_coin = int(input("Insert Coin: "))
    # check if amount is valid coin denomination, use a list
    if user_coin in [5, 10, 25]:
    # subtract that coin from the amount due
        amount_due = amount_due - user_coin

# Once loop is broken, calculate and output change due

print("Change Owed:", abs(amount_due))




