# Type hints
def meow(n: int) -> None:
    # Will raise an error in mypy due to the function not returning a value, only printing. 
    for _ in range(n):
        print("meow")

def meow2(n: int) -> str:
    return "meow\n" * n






number: int = int(input("Number: "))
meows: str = meow2(number)
print(meows, end="")