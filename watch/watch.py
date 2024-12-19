import re

# Structure watch.py as follows, wherein you’re welcome to modify main and/or implement other functions as you see fit, but you may not import any other libraries.
# You’re welcome, but not required, to use re and/or sys.
def main():
    print(parse(input("HTML: ")))


# Constraints:________________________________________________________________________________
# expects a str of HTML as input.
# extracts any YouTube URL that’s the value of a src attribute of an iframe element therein.
# returns its shorter, shareable youtu.be equivalent as a str.
# Assume that the value of src will be surrounded by double quotes.
# assume that the input will contain no more than one such URL.
# Assume URL will be in these formats
    # https://www.youtube.com/embed/xvFZjo5PgG0
    # http or https
    # www.youtube or youtube
# If the input does not contain any such URL at all, return None.
# ____________________________________________________________________________________________
def parse(s):
    match_src = None
    match_src = re.search(r".*?src=\"https?://(?:www\.)?youtube\.com(.*?)\".*?", s)
    if match_src is not None:
        parse_list = match_src.group(1).split("/")
        return f"https://youtu.be/{parse_list[-1]}"
    else:
        return "None"


if __name__ == "__main__":
    main()
