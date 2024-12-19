# Promt user for name of file
fileType = input("Hey buddy. What's yer file name?  ").strip().lower()

# Output media type if file type is known
if fileType.endswith(".gif"):
    print("image/gif")

elif fileType.endswith(".jpg") or fileType.endswith(".jpeg"):
    print("image/jpeg")

elif fileType.endswith(".png"):
    print("image/png")

elif fileType.endswith(".pdf"):
    print("application/pdf")

elif fileType.endswith(".zip"):
    print("application/zip")

elif fileType.endswith(".txt"):
    print("text/plain")

# Output if file type is unknown
else: print("application/octet-stream")
