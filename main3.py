import argparse
import json
from sys import argv
from time import time
import math


def parse_args():
	parser = argparse.ArgumentParser()
	parser.add_argument("-f", action="store", nargs="?", default="data.json")
	parser.add_argument("-lat", action="store", nargs="+", default="55.753283")
	parser.add_argument("-long", action="store", nargs="+", default="37.620723")
	args = parser.parse_args(argv[1:])
	return vars(args)


def load_data(file):
	try:
		return json.load(open(file))
	except FileNotFoundError:
		print("FileNotFound...")
		exit(0)


def get_closest_cafe(data, latitude, longitude, count=12648):
	distance = math.sqrt(
		(latitude - data[0]["geoData"]["coordinates"][0]) ** 2 + ((longitude - data[0]["geoData"]["coordinates"][1]) ** 2)
	)
	i = 0
	for g in range(1, count):
		place_lat = data[g]["geoData"]["coordinates"][0]
		place_long = data[g]["geoData"]["coordinates"][1]
		a = math.sqrt((latitude-place_lat)**2+((longitude-place_long)**2))
		if distance > a:
			distance = a
			i = g
		else:
			continue
	return print(distance, data[i]["Name"])


if __name__ == "__main__":
	start = time()

	arguments = parse_args()
	f = arguments["f"]
	data = load_data(f)

	latitude = float(arguments["lat"])
	longitude = float(arguments["long"])

	get_closest_cafe(data, latitude, longitude)
	end = time()
	print("Execution time:", end-start, sep="")
