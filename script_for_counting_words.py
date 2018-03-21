import re
import argparse
from sys import argv

def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("-f", action="store", default="data.txt", nargs="?")

    args = parser.parse_args(argv[1:])

    return vars(args)


def main(data):
    pattern = r"\w+"
    try:
        d = open(data, "r")
    except FileNotFoundError:
        print("FileNotFound")
    info = d.read()
    list_of_words = re.findall(pattern, info)

    for word in range(len(list_of_words)):
        list_of_words.count(list_of_words[word])
        dict
    d.close()
    return 0


if __name__ == "__main__":
    parse_args()

    file = parse_args()["f"]

    main(file)
