import argparse
import sys
import os


class EmptyFileError(Exception):
	pass


def parse_args():
	parser = argparse.ArgumentParser()
	parser.add_argument("--ph", action="store", nargs="?", default="3.py")
	args = parser.parse_args(sys.argv[1:])
	return vars(args)


def read_from_file(ph):
	try:

		size = os.path.getsize(ph)
		if size < 1:
			raise EmptyFileError

		with open(ph) as f:
			print(type(f))
			for line in f:
				print(line.rstrip(), end=" ")

	except FileNotFoundError:
		print("File not found")

	except PermissionError:
		print("Not enough permissions")

	except EmptyFileError:
		print("Empty file")


if __name__ == "__main__":
	args = parse_args()

	ph = args["ph"]

	read_from_file(ph)