import emoji

getInput = input("Input: ")
getInput = emoji.emojize(getInput, language="alias")
print ("Output: ", getInput)

