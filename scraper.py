from bs4 import BeautifulSoup
import requests
import re
import json
import pandas

# Getting the data from the URL
headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '3600',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
}

# url = "http://example.com"
# url = "https://scoresaber.com/u/76561197990446328"
# req = requests.get(url, headers)
# leaderboard = {}


def fetch_leaderboard(url_list):
    leaderboard = {}
    for url in url_list:
        content = requests.get(url, headers).content
        soup = BeautifulSoup(content, 'html.parser')
        # print(soup.prettify())
        player_name = soup.find(
            "meta", property="og:title").attrs["content"].partition("'")[0]
        player_dict = {
            "Player Name": player_name
        }
        information_list = soup.find(
            "meta", property="og:description").attrs["content"].split("\n  ")
        for information in information_list:
            if information.partition(": ")[0] == "Performance Points":
                player_dict[information.partition(
                    ": ")[0]] = float(re.sub(r"[^0-9\.]", "", information.partition(": ")[2]))
            else:
                player_dict[information.partition(
                    ": ")[0]] = int(re.sub(r"[^0-9\.]", "", information.partition(": ")[2]))
        # print(player_dict)
        leaderboard[url] = player_dict
    df = pandas.DataFrame(leaderboard)
    df = df.sort_values(by="Player Ranking", axis=1)
    # print(df)
    leaderboard_json = df.to_json()
    leaderboard_json = leaderboard_json.replace("\\/", "/")
    return leaderboard_json


# print(fetch_leaderboard(["https://scoresaber.com/u/76561197995954197", "https://scoresaber.com/u/76561197996506539", "https://scoresaber.com/u/76561197990446328"])
#       )
# }
# .split("\n  ")
# player_ranking = re.search("")
# meta_description_list = meta_description.attrs["content"].split("\n  "))
