import requests
import bs4
import json


def getUser(id):
    stdJson = downloadDataByMode(id, "osu")
    taikoJson = downloadDataByMode(id, "taiko")
    ctbJson = downloadDataByMode(id, "fruits")
    maniaJson = downloadDataByMode(id, "mania")

    user = processJson(stdJson, taikoJson, ctbJson, maniaJson)

    return user


def processJson(std, taiko, ctb, mania):
    medals = list(map(lambda x: x["achievement_id"], std["user_achievements"]))

    return {"id": std["id"],
            "name": std["username"],
            "pp_raw": [std["statistics"]["pp"],
                       taiko["statistics"]["pp"],
                       ctb["statistics"]["pp"],
                       mania["statistics"]["pp"]
                       ],
            "country_code": std["country"]["code"],
            "medals_count": len(medals),
            "badges_count": len(std["badges"]),
            "medals": medals,
            "stdranks": std["statistics"]["rank"],
            "taikoranks": taiko["statistics"]["rank"],
            "ctbranks": ctb["statistics"]["rank"],
            "maniaranks": mania["statistics"]["rank"],
            "lovedmaps": std["loved_beatmapset_count"],
            "rankedmaps": std["ranked_and_approved_beatmapset_count"],
            "replays": std["statistics"]["replays_watched_by_others"]
            + taiko["statistics"]["replays_watched_by_others"]
            + ctb["statistics"]["replays_watched_by_others"]
            + mania["statistics"]["replays_watched_by_others"],
            "avatar_url": std["avatar_url"]
            }


def downloadDataByMode(id, mode, jsonId="json-user"):
    link = "https://osu.ppy.sh/users/" + str(id) + "/" + str(mode)
    res = requests.get(link).text
    open("test.txt", "w").write(str(res.encode("utf-8")))
    soup = bs4.BeautifulSoup(res, "html.parser")
    array = soup.find("script", {"id": jsonId}).string.strip()
    arr = json.loads(array)
    return arr
