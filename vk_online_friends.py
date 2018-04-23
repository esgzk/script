import requests
import re
from time import sleep


def check_input_id():
    digits = re.findall(r"\d{9}", input("Write VK's id:\t"))

    try:
        return digits[0]
    except IndexError:
        print("Invalid id")
        print("########################")


def main(user_id):
    if user_id:
        access_token = ""
        r = requests.get("https://api.vk.com/method/friends.get?v=5.8&access_token=" + access_token + "&fields=online" +
                         "&user_id=" + user_id)
        for i in range(r.json()["response"]["count"]):
            if r.json()["response"]["items"][i]["online"] == 1:
                print("Online friend: " +
                      r.json()["response"]["items"][i]["first_name"], r.json()["response"]["items"][i]["last_name"])


if __name__ == "__main__":
    while True:
        main(check_input_id())
        sleep(1)





