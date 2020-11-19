import requests
import bs4 as bs
import json
import urllib.request
import urllib.error

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


def downloadDataByMode(id, mode):
    headers = {'Authorization':'Bearer APIV2TOKEN'}
    oApiRequest = requests.get('https://osu.ppy.sh/api/v2/users/'+str(id)+'/'+str(mode), headers=headers)
    print("downloaded user: " + oApiRequest.text[0:50]);
    return json.loads(oApiRequest.text)

def downloadMedalDataByMode(id, mode, jsonId="json-user"):
    uClient = urllib.request.urlopen("https://osu.ppy.sh/users/" + str(id) + "/" + str(mode))
    page_html = uClient.read()
    uClient.close()
    page_soup = bs.BeautifulSoup(page_html, "html.parser")
    container = page_soup.find("script", {"id": jsonId})
    container = str(container);
    container = container.replace('<script id="' + jsonId + '" type="application/json">', "")
    container = container.replace("</script>", "")
    array = container.strip()
    data = json.loads(array)
    return data
