#main function
def main():
    question=input("How's it going? ")
    convert(question)

#convert function that converts emoticons to emojis
def convert(text):
    print(text.replace(":)", "🙂").replace(":(", "🙁"))

#Duh...Call your function
main()
