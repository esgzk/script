import argparse
import json
import requests
import time
from sys import argv
#---------------------
def parse_args():
	parser = argparse.ArgumentParser()
	parser.add_argument("-f", action="store", nargs="?", default="data.json")
	args = parser.parse_args(argv[1:])
	return vars(args)


def read_from_file(f):
	try:
		data = json.load(open(f))
		return data
	except FileNotFoundError:
		print("File Not Found...")
		exit(0)


def main(data):
	responseforlength = requests.post(
	"https://apidata.mos.ru/v1/datasets/1903?api_key=21547744ee7b8b5efe3a428c5670b583")
	count = int(responseforlength.json()["ItemsCount"])

	for g in range(count):
			seats.append(data[g]["SeatsCount"])
			names.append(data[g]["Name"])

	database = dict(zip(seats, names))
	print(database[max(seats)])


if __name__ == "__main__":
	start = time.time()
	seats = []
	names = []

	f = parse_args()
	argt = f["f"]
	data = read_from_file(argt)

	main(data)
	end = time.time()
	print(end-start)