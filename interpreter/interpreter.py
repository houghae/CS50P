# Promt user for math expression
# Assume input formatted as (x y z)
expression = input("I'm a calc. Feed me an expression  ").strip()
x, y, z = expression.split(" ")

x = int(x)
z = int(z)

# Calculate and output result as float to tenths decimal place
match y:
    case "+":
        print(round(float(x+z), 1))
    case "-":
        print(round(float(x-z), 1))
    case "/":
        print(round(float(x/z), 1))
    case "*":
        print(round(float(x*z), 1))

