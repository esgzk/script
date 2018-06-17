import requests
import datetime
import argparse
import re
import json


def time_checker(func):
    def wrapper(*args, **kwargs):
        start = datetime.datetime.now()
        func_result = func(*args, **kwargs)
        print("TIME:", datetime.datetime.now() - start)
        return func_result
    return wrapper


def get_args():
    argparser = argparse.ArgumentParser()
    argparser.add_argument("-l", default=None, help="Your e-mail login")
    argparser.add_argument("-p", default=None, help="Your password")
    argparser.add_argument("-speed", default=None, choices=range(300, 1001, 50), type=int, help="New tariff to set")
    argparser.add_argument("-pspeed", default=None, help="previous tariff", type=int, choices=range(300, 1001, 50))
    args = argparser.parse_args()
    return vars(args)


def getUidByMail(mail):
    url = "https://my.yota.ru/selfcare/login/getUidByMail"
    response = requests.post(url, data={"value": mail})
    result = response.text
    login = result[3:]
    return login


def enter(login, password, mail):
    url = "https://login.yota.ru/UI/Login"
    params_for_signing_in = {
        "IDToken1": login,
        "IDToken2": password,
        "goto": "https://my.yota.ru:443/selfcare/loginSuccess",
        "gotoOnFail": "https://my.yota.ru:443/selfcare/loginError",
        "org": "customer",
        "ForceAuth": "true",
        "login": mail,
        "password": password,
    }
    response = requests.post(url, data=params_for_signing_in)
    return response.status_code


def login_success():
    r = requests.get("https://my.yota.ru/selfcare/loginSuccess")
    return r.status_code


@time_checker
def sign_in(password, mail, speed, pspeed):
    login = getUidByMail(mail)
    if login:
        if enter(login, password, mail) == 200:
            if login_success() == 200:
                print("Successfully signed in!")
                if testDriveStatus() == 200:
                    if changeOffer(speed, pspeed) == 200:
                        print(f"Successfully change from {pspeed} to {speed}")
                        logout()
                    else:
                        print("Changing goes wrong...")
                        exit(0)
                else:
                    print("Test DriveStatus goes wrong...")
                    exit(0)
            else:
                print("Checking logging goes wrong...")
                exit(0)
        else:
            print("Logging goes wrong...")
            exit(0)
    else:
        print("Getting ID goes wrong...")
        exit(0)


def testDriveStatus():
    url = "https://my.yota.ru/selfcare/devices/testDriveStatus"
    r = requests.post(url)
    return r.status_code


def changeOffer(speed, pspeed):
    try:
        with open("config.cfg", "r", encoding="utf-8") as sliderdata:
            r = sliderdata.read()
            match = re.search("var sliderData =(.*);", r)
            if match:
                device = json.loads(match.group(1))
                product = list(device)[0]
                offer = next(x for x in device[product]["steps"] if x["amountNumber"] == str(pspeed))
                period = offer["remainNumber"] + " " + offer["remainString"]
                position = offer["position"]
                offer = next(x for x in device[product]["steps"] if x["amountNumber"] == str(speed))
                offercode = offer["code"]
                status = device[product]["status"]
                productid = device[product]["productId"]
            else:
                print("I swear the God, it shouldn't has happened ¯\_(ツ)_/¯ ")
                exit(0)
    except FileNotFoundError:
        print("Please copy config file to same folder with script")
        exit(0)
    except StopIteration:
        print("Undefined behavior ¯\_(ツ)_/¯")
        exit(0)

        url = "https://my.yota.ru/selfcare/devices/changeOffer"
    params_for_changing_offer = {
        "product": productid, # <-- productId every time changed
        "offerCode": offercode,
        "areOffersAvailable": "false",
        "period": period,
        "status": status,
        "autoprolong": "1",
        "isSlot": "false",
        "finished": "false",
        "blocked": "false",
        "freeQuotaActive": "false",
        "pimpaPosition": position,
        "specialOffersExpanded": "false",
        "resourceId": "",  # <-- unique for every account, please change it
        "currentDevice": "0",
        "username": "",
        "isDisablingAutoprolong": "false"
    }
    response = requests.post(url, data=params_for_changing_offer)
    return response.status_code


def logout():
    url = "https://my.yota.ru/selfcare/logout"
    r1 = requests.get(url)
    url = "https://login.yota.ru/UI/Logout?goto=http%3A%2F%2Fwww.yota.ru%2F"
    r2 = requests.get(url)
    if r1.status_code == 200 and r2.status_code == 200:
        print("Logout done!")
    else:
        print("Logout hasn't done")
        exit(0)


if __name__ == "__main__":
    arguments = get_args()
    sign_in(arguments['p'], arguments['l'], arguments["speed"], arguments["pspeed"])
