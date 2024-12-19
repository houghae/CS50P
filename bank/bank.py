
# Greet customer, ask for input
greeting = input("Howdy, partner!").strip().lower()

# If greeting starts with 'hello', ouput $0
if greeting.startswith("hello"):
    print("$0")

# If starts with 'h', output $20
elif greeting.startswith("h"):
    print("$20")

# Otherwise output $100
else: print("$100")

