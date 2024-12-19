import sys
import requests
import json


# specify number of bitcoins, n, as command line argument
# If argument can't be converted to float, exit with error message
#DONE
try:
    n = float(sys.argv[1])
except IndexError:
    sys.exit("Missing command-line argument")
except ValueError:
    sys.exit("Command-line argument is not a number")


# querie API, catch exceptions
try:
    bitcoinPrice = requests.get("https://api.coindesk.com/v1/bpi/currentprice.json")
except requests.RequestException:
    print("Request exception error occured")
    pass


# store JSON file, grab USD float from JSON, multiply price by argument input
btcJSON = bitcoinPrice.json()
currentValue = btcJSON["bpi"]["USD"]["rate_float"]
userValue = currentValue * n


# output cost of n bitcoins in USD
print(f"${userValue:,.4f}")




