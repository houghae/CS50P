
class Jar:
    # __init__ should initialize a cookie jar with the given capacity, which represents the maximum number of cookies that can fit in the cookie jar.
    def __init__(self, capacity=12):
        self.capacity = capacity
        self.size = 0

    # __str__ should return a str with n 🍪, where n is the number of cookies in the cookie jar.
    # For instance, if there are 3 cookies in the cookie jar, then str should return "🍪🍪🍪"
    def __str__(self):
        if self.size == 0:
            return ""
        else:
            return self.size * "🍪"

    # deposit should add n cookies to the cookie jar. If adding that many would exceed the cookie jar’s capacity, though, deposit should instead raise a ValueError.
    def deposit(self, n):
        if self.size + n <= self.capacity:
            self.size += n
        else:
            raise ValueError("Too many cookies")

    # withdraw should remove n cookies from the cookie jar. Nom nom nom.
    # If there aren’t that many cookies in the cookie jar, though, withdraw should instead raise a ValueError.
    def withdraw(self, n):
        if n <= self.size:
            self.size -= n
        else:
            raise ValueError("Not enough cookies")

    # capacity should return the cookie jar’s capacity.
    @property
    def capacity(self):
        return self._capacity

    # If capacity is not a non-negative int, though, __init__ should instead raise a ValueError.
    @capacity.setter
    def capacity(self, capacity):
        if capacity < 0 or not isinstance(capacity, int):
            raise ValueError("Must be 0 or positive integer")
        else:
            self._capacity = capacity

    # size should return the number of cookies actually in the cookie jar, initially 0.
    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, size):
        self._size = size

def main():
    jar = Jar(15)
    jar.deposit(10)
    print(jar.size)
    jar.withdraw(5)
    print(jar.size)
    jar.deposit(6)
    print(jar.size)
    jar.deposit(4)
    print(jar.size)
    jar.withdraw(10)
    print(str(jar))


if __name__ == "__main__":
    main()

