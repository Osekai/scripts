import requests
import bs4
from time import sleep
import logger


def getUsersFromLeaderboards(count):
    users = []
    for mode in ["osu", "taiko", "fruits", "mania"]:
        logger.Log("Downloading leaderboard from " + mode)
        for page in range(count):
            users += downloadLeaderboard(mode, page)
            sleep(2)
    return users


def downloadLeaderboard(mode, page):
    link = "https://osu.ppy.sh/rankings/" + mode + \
        "/performance?page=" + str(page+1) + "#scores"
    try:
        return extractUsers(requests.get(link).text)
    except Exception as err:
        print(str(mode) + " - " + str(page) + " failed\n" + str(err))
        return []


def extractUsers(site):
    soup = bs4.BeautifulSoup(site, 'html.parser')
    users = []
    for div in soup.find_all("div", {"class": "ranking-page-table__user-link"}):
        userId = int(div.find_all("a")[-1].get('data-user-id'))
        users.append(userId)
    return users
