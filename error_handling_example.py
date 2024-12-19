import sys
from PIL import Image, ImageOps
import os
valid_ext = [".jpg", ".jpeg", ".png"]
output_size = (600, 600)

def main():
    error_handling()
    overlay()

# BEST ERROR HANDLING I'VE DONE YET. It returns back to main to keep error handling separate. Love this.
def error_handling():
    # Expect two command line arguments
    if len(sys.argv) < 3:
        sys.exit("Too few command-line arguments")
    elif len(sys.argv) > 3:
        sys.exit("Too many command-line arguments")
    # Valid file extension. jpg, jpeg, or png, case-insensitive
    elif any(sys.argv[2].lower().endswith(ext) for ext in valid_ext) is False:
        sys.exit("Invalid output")
    # Input and output have different extension types
    elif ext_type(sys.argv[1]) != ext_type(sys.argv[2]):
        sys.exit("Input and output have different extensions")
    else:
        try:
            if os.path.isfile(sys.argv[1]) == False:
                raise FileNotFoundError
            else:
                return
        # First argument doesn't exist
        except FileNotFoundError:
            sys.exit("Input does not exist")


def ext_type(arg):
    _, ext = os.path.splitext(arg)
    return ext


def overlay():
    image = Image.open(sys.argv[1])
    image = ImageOps.fit(image, output_size)
    size = image.size
    shirt = Image.open("shirt.png")
    fit_image = ImageOps.fit(shirt, size)
    image.paste(fit_image, fit_image)
    image.save(sys.argv[2])




if __name__ == "__main__":
    main()

