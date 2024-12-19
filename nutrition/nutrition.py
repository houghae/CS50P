# Create dict for top 20 fruits

fruits = {
    "apple" : 130,
    "avocado" : 50,
    "banana" : 110,
    "cantaloupe" : 50,
    "grapefruit" : 60,
    "grapes" : 90,
    "honeydew melon" : 50,
    "kiwifruit" : 90,
    "lemon" : 15,
    "lime" : 20,
    "nectarine" : 60,
    "orange" : 80,
    "peach" : 60,
    "pear" : 100,
    "pineapple" : 50,
    "plums" : 70,
    "strawberries" : 50,
    "sweet cherries" : 100,
    "tangerine" : 50,
    "watermelon" : 80,
}




# Promt user for fruit input, output calories associated with that fruit
# Make case insensitive. Use lower case str method
# Ignore inputs not in the dict

fruitType = input("Fruit type? ").lower()

if fruitType in fruits:
    print(fruits[fruitType])
else:
    print(end="")
