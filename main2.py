import argparse
import json
import requests
import time
from sys import argv
#---------------------
#---------------------
def parse_args():
	"""
	create argument for give file to program
	:return:dict of arguments that were created
	"""
	parser = argparse.ArgumentParser()
	parser.add_argument("-f", action="store", nargs="?", default="data.json")
	parser.add_argument("-long", action="store", nargs="+", default="55.751942")
	parser.add_argument("-lat", action="store", nargs="+", default="37.617323")
	args = parser.parse_args(argv[1:])
	return vars(args)


def read_from_file(f):
	"""
	read json data from file
	:return:data
	"""
	try:
		data = json.load(open(f))
		return data
	except FileNotFoundError:
		print("File Not Found...")
		exit(0)


def count_of_places():
	"""
	get count of places
	:return: count
	"""
	responseforlength = requests.post(
		"https://apidata.mos.ru/v1/datasets/1903?api_key=21547744ee7b8b5efe3a428c5670b583"
	)
	count = int(responseforlength.json()["ItemsCount"])
	return count


def main(data, latitude, longitide, count):
	"""
	pass
	:param data:
	:param latitude:
	:param longitide:
	:return:
	"""
	for g in range(5):
		geo_2 = str(data[g]["geoData"]["coordinates"][0])
		geo_1 = str(data[g]["geoData"]["coordinates"][1])
		url = "https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins=" + longitude + "," + latitude + "&destinations=" + geo_1 + "," + geo_2 + "&mode=walking&key=AIzaSyBjk1p4jrUJU_KeY71aT-Mq9nMcEub1BjY"
		r = requests.get(url)
		distance.append(r.json()["rows"][0]["elements"][0]["distance"]["text"])
		timeto.append(r.json()["rows"][0]["elements"][0]["duration"]["text"])
	print(distance, timeto)
	minlen = distance.index(min(distance))


# def geolocation():
# 	r = requests.get(
# 		"https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins=58.613062, 49.666269&destinations=55.879001531303373,37.714565000436&mode=walking&key=AIzaSyBjk1p4jrUJU_KeY71aT-Mq9nMcEub1BjY"
# 	)
# 	if r.json()["rows"][0]["elements"][0]["status"] == "ZERO_RESULTS":
# 		print("Bad... ", "HTTP_CODE:", r.status_code, sep="")
# 		exit(0)
# 	elif r.json()["rows"][0]["elements"][0]["status"] == "NOT_FOUND":
# 		print("Bad... ", "HTTP_CODE:", r.status_code, sep="")
# 		print("NOT_FOUND")
# 		exit(0)
# 	else:
# 		print("Good... ", "HTTP_CODE:", r.status_code, sep="")
# 		print(r.json()["rows"][0]["elements"][0]["distance"]["text"])#Расстояние до места в милях
# 		print(r.json()["rows"][0]["elements"][0]["duration"]["text"], "on foot")#Время пешком до места
# 		print(r.json())


def geodata():
	pass


if __name__ == "__main__":
	start = time.time()
	distance = []
	timeto= []
	args = parse_args()
	argument = args["f"]
	longitude = args["long"]
	latitude = args["lat"]

	data = read_from_file(argument)
	count = count_of_places()


	main(data, longitude, latitude, count)
	end = time.time()
	print("Executable time:", end-start, sep="")
	#api AIzaSyBjk1p4jrUJU_KeY71aT-Mq9nMcEub1BjY
	#api AIzaSyCuUTA_3WknpAyHag20CUFU1NyGQyR4Usw


