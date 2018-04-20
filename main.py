import requests
import re


def check_input_id():
    digits = re.findall(r"\d", input("Write VK's id:\n"))
    string = ""
    for digit in digits:
        string += str(digit)
    return string


def main(user_id):
    access_token = ""
    r = requests.get("https://api.vk.com/method/friends.get?v=5.8&access_token=" + access_token + "&fields=online" +
                                                                                                  "&user_id=" + user_id)

    for i in range(r.json()["response"]["count"]):
        if r.json()["response"]["items"][i]["online"] == 1:
            print(r.json()["response"]["items"][i]["first_name"], r.json()["response"]["items"][i]["last_name"])


if __name__ == "__main__":
    main(check_input_id())






