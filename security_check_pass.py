import argparse
from sys import argv


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", action="store", default="1234")
    parser.add_argument("-f", action="store", default="10-million-password-list-top-1000000.txt")
    args = parser.parse_args(argv[1:])

    return vars(args)


def check_in_list(password, path_to_bad_passwords_file):
    try:
        with open(path_to_bad_passwords_file, "r") as f:
            if f.readline() == password:
                score = 0
                print("BadPassword")
                return 1
            else:
                f.readline()
    except FileNotFoundError:
        return 0



def check_pass(password):
    score = 0
    if any(symbol for symbol in password if symbol in password.ascii_lowercase):
        score += 1
        


def main(password):

    if check_in_list(password, path_to_bad_passwords_file=password):
        exit(0)
    else:
        check_pass(password)


if __name__ == "__main__":
    args = parse_args()
    main(args["p"])
