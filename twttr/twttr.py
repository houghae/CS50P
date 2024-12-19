
def main():
    sansVowels = shorten(input("Input: "))
    print("Output:", sansVowels)


def shorten(word):
    vowels = ["a", "e", "i", "o", "u", "A", "E", "I", "O", "U"]
    return "".join(i for i in word if i not in vowels)


if __name__ == "__main__":
    main()
