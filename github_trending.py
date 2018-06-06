import requests
import datetime


def shifted_time(days):
    current_date = datetime.datetime.now()
    new_date = datetime.timedelta(days=days)

    return current_date - new_date


def get_users(date):
    users = []
    formated_date = date.strftime("%Y-%m-%d")
    params = {
        'q': str(formated_date),
        'sort': 'stars',
        'order': 'desc'
    }
    r = requests.get("https://api.github.com/search/repositories", params=params)
    for i in range(20):
        login_name = r.json()["items"][i]["owner"]["login"]
        repository_name = r.json()["items"][i]["name"]
        user = (login_name, repository_name)
        users.append(user)

    return users


def get_issues(users):
    params_for_oauth = {
        "username": "esgzk"
    }
    requests.get("https://api.github.com/user", params=params_for_oauth)
    for user in users:
        login_name, repos_name = user[0], user[1]
        url = "https://api.github.com/repos/{0}/{1}/issues?q=state:open+type:issue&sort=created&order=desc".format(
            login_name, repos_name)
        r = requests.get(url)
        issues = r.json()
        print("\"{0}'s:\" issues\n".format(repos_name))
        for issue in issues:
            title = issue["title"]
            print(f"\t\t issue includes:\" {title}\"")


if __name__ == "__main__":
    get_issues(get_users(shifted_time(0)))
