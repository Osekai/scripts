import user_download


def GetMedals(userId):
    json = user_download.downloadDataByMode(userId, "osu", "json-achievements")
    medalMetaData = []
    for medalInf in json:
        medal = {}
        medal["medalid"] = medalInf["id"]
        medal["name"] = medalInf["name"].replace('"', "'")
        medal["link"] = medalInf["icon_url"].replace('"', "'")
        medal["description"] = medalInf["description"].replace('"', "'")
        medal["restriction"] = medalInf["mode"]
        medal["grouping"] = medalInf["grouping"]
        medal["ordering"] = medalInf["ordering"]
        medal["instructions"] = medalInf["instructions"]
        for key in medal.keys():
            if medal[key] is None:
                medal[key] = "NULL"
        medalMetaData.append(medal)
    return medalMetaData
