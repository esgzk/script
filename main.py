import requests
import math
import time
def main():
	responseforlength = requests.post("https://apidata.mos.ru/v1/datasets/1903?api_key=21547744ee7b8b5efe3a428c5670b583")
	count = int(responseforlength.json()["ItemsCount"])#Кол-во всего мест общепита
	#r = requests.get("https://apidata.mos.ru/v1/datasets?api_key=21547744ee7b8b5efe3a428c5670b583")
	#print(r.json())
	# r = requests.post("https://apidata.mos.ru/v1/datasets?api_key=21547744ee7b8b5efe3a428c5670b583&$skip=1&$top=1&$inlinecount=allpages")
	# print(r.json()["Items"][0]["Caption"])
	var = 500
	start = time.time()
	rest = count - math.floor(count/500)*500#Остаток с помощью которого fixсим вылет с range, т.к обработка по 500 шт
	for i in range(1, math.ceil(count/500)):
		r = requests.post("https://apidata.mos.ru/v1/datasets/1903/rows?api_key=21547744ee7b8b5efe3a428c5670b583&$top=500&$skip=" + str(var*i))#запрос на определенное кол-во мест общепита
		print(r.json())
		for g in range(0, 500):
			try:
				seats.append(r.json()[g]["Cells"]["SeatsCount"])#Места fetchит из полученного ответа с №1 по №500
				names.append(r.json()[g]["Cells"]["Name"])
				# print(r.json()[g]["Number"])#Checker
			except:
				if IndexError:
					for j in range(rest):
						seats.append(r.json()[j]["Cells"]["SeatsCount"])
	print(max(seats))
	end = time.time()
	print(end-start)
	database = dict(zip(seats,names))
	print(database[1500])



# def response_file():
# 	file = open("response.txt", "w+")
# 	r = requests.post("https://apidata.mos.ru/v1/datasets/1903/rows?api_key=21547744ee7b8b5efe3a428c5670b583&$top=500")
# 	file.write(str(r.json()))
# 	file.close()



# def read_from_file(filetoopen):
# 	file = open(filetoopen, "r")
# 	content = file.read()
# 	print(list(content))
# 	file.close()





if __name__ == "__main__":
	names = []
	seats = []
	main()
	# response_file()
	# read_from_file("response.txt")