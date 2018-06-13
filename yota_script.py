import argparse
import urllib
from urllib import request
import http.cookiejar
import re
import json

def get_args():

    argparser = argparse.ArgumentParser()
    argparser.add_argument("-l", default=None, help="login")
    argparser.add_argument("-p", default=None, help="password")
    argparser.add_argument("-speed", help="speed_to_set", choices=range(250, 1001, 50), type=int)
    args = argparser.parse_args()

    return vars(args)


# def get_credentials():
#     try:
#         with open("config.json", "r") as config_file:
#             cfg = json.load(config_file)
#             login = cfg["login"]
#             password = cfg["password"]


def parse_device(page):
    slider = parse_slider(page)
    product = list(slider)[0]

    return slider[product]


def parse_slider(page):
    page = page.split("\n")

    for line in page:
        match = re.search(".*var sliderData =(.*);", line)
        if match:
            return json.loads(match.group(1))

    unavailable = "Личный кабинет временно недоступен"
    for line in page:
        match = re.search(".*{}.*".format(unavailable), line)
        if match:
            print(unavailable)
            exit(0)

    print("slider data not found in page")
    exit(0)


def change(speed, device, cj):
    offer = next(x for x in device["steps"] if x["amountNumber"] == speed)
    remain = offer["remainNumber"] + " " + offer["remainString"]
    product_id = device["productId"]

    url = "https://my.yota.ru/selfcare/devices/changeOffer"
    params = {
        "product": product_id,
        "offerCode": offer["code"],
        "areOffersAvailable": "false",
        "period": remain,
        "status": device["status"],
        "autoprolong": "1",
        "isSlot": "false",
        "resourceId": "",
        "currentDevice": "0",
        "username": ""
    }

    data = urllib.parse.urlencode(params)
    data = data.encode('utf-8')
    opener = request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    current_product = device["current_product"]
    print("Changing plan from {} {} to {} {}".format(current_product["amountNumber"], current_product["amountString"],
                                                     offer["amountNumber"], offer["amountString"]))
    print("Time remaining: {}".format(remain))


def sign_in(login, password):
    url = "https://my.yota.ru/selfcare/login"
    params = {
        "IDToken1": login,
        "IDToken2": password,
        "goto": "https://my.yota.ru:443/selfcare/devices"
    }

    data = urllib.parse.urlencode(params)
    data = data.encode('utf-8')

    cj = http.cookiejar.CookieJar()
    opener = request.build_opener(urllib.request.HTTPCookieProcessor(cj))

    response = opener.open(url, data)

    page = response.read().decode("utf-8")
    device = parse_device(page)

    return page, device, cj


if __name__ == "__main__":
    arguments = get_args()
    # get_credentials()
    args = sign_in(arguments["-l"], arguments["-p"])
    page = args[0]
    device = args[1]
    parse_device(page)
    change(arguments["-speed"], device, args[2])
