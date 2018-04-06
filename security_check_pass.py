import argparse
from sys import argv
import string
from time import time


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", action="store", default="password")
    parser.add_argument("-f", action="store", default="10-million-password-list-top-1000000.txt")
    arguments = parser.parse_args(argv[1:])
    return vars(arguments)


def check_in_list(password, path_to_bad_passwords_file):
    try:
        with open(path_to_bad_passwords_file, "r") as f:
            for i in range(1000000):
                if str(f.readline()).strip() == password:
                    print("BadPassword")
                    return 1
    except FileNotFoundError:
        return 0


def check_pass(password):
    score = 0
    length = len(password)

    if any(symbol for symbol in password if symbol in string.ascii_lowercase):
        score += 1
    if any(symbol for symbol in password if symbol in string.ascii_uppercase):
        score += 1
    if any(symbol for symbol in password if symbol in string.digits):
        score += 1
    if any(symbol for symbol in password if symbol in string.punctuation):
        score += 1
    if 3 < length < 8:
        score += 1
    if 8 < length < 14:
        score += 2
    if 14 < length < 20:
        score += 3
    if length >= 20:
        score += 4
        
    return score


def main(password, path_to_vocabulary_of_bad_pass):
    if check_in_list(password, path_to_bad_passwords_file=path_to_vocabulary_of_bad_pass):
        end = time()
        print(end - start)
        exit(0)
    else:
        print(check_pass(password))
        end = time()
        print(end - start)


if __name__ == "__main__":
    start = time()
    args = parse_args()
    main(args["p"], args["f"])