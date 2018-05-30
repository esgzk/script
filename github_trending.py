import requests
import datetime

def shifted_time(days):
    current_date = datetime.datetime.now()
    new_date = datetime.timedelta(days=days)

    return current_date - new_date


def get(date):
    formated_date = date.strftime("%Y-%m-%d")
    params = {
        'q': str(formated_date),
        'sort':'starts',
        'order':'desc'
    }
    r = requests.get("https://api.github.com/search/repositories", params=params)
    repository_name = r.json()["items"][0]["name"]
    login_name = r.json()["items"][0]["owner"]["login"]
    return repository_name, login_name


def get_issues(repos_name, login_name):
    url = "https://api.github.com/repos/{0}/{1}/issues".format(login_name, repos_name)
    print(url)
    #r = requests.get(url)
    #return print(r.json())


if __name__ == "__main__":
    list_of_names = get(shifted_time(7))
    get_issues(list_of_names[0], list_of_names[1])


