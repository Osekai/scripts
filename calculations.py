from math import sqrt

def getRarestMedal(user, medalRates):
    for medal in medalRates:
        if medal["id"] in user["medals"]:
            return medal["id"]

def getMedalRarity(userData):
    allMedals = []
    medalOccurence=[]
    for medals in map(lambda x: x["medals"], userData):
        try:
            allMedals.extend(medals)
        except:
            print("Some medals didn't get included: " + medals)

    individualMedals = set(allMedals)
    medalOccurence = list(map(lambda x: {"medal":x, "count":allMedals.count(x)}, individualMedals))
    medalRates = list(map(lambda x: {"id":x["medal"], "frequency": (100*x["count"]/len(userData))}, medalOccurence))

    return medalRates

def combineData(user, rarestMedal, ppstats):
    finalData = {}
    finalData["id"] = user["id"]
    finalData["name"] = user["name"]
    finalData["country_code"] = user["country_code"]

    finalData["total_pp"] = ppstats["totalpp"]
    finalData["stdev_pp"] = ppstats["stdevpp"]
    finalData["standard_pp"] = ppstats["standardpp"]
    finalData["taiko_pp"] = ppstats["taikopp"]
    finalData["ctb_pp"] = ppstats["ctbpp"]
    finalData["mania_pp"] = ppstats["maniapp"]

    finalData["standard_global"] = user["stdranks"]["global"]
    finalData["taiko_global"] = user["taikoranks"]["global"]
    finalData["ctb_global"] = user["ctbranks"]["global"]
    finalData["mania_global"] = user["maniaranks"]["global"]
    finalData["standard_country"] = user["stdranks"]["country"]
    finalData["taiko_country"] = user["taikoranks"]["country"]
    finalData["ctb_country"] = user["ctbranks"]["country"]
    finalData["mania_country"] = user["maniaranks"]["country"]

    finalData["medal_count"] = user["medals_count"]
    finalData["badge_count"] = user["badges_count"]
    finalData["rarest_medal"] = rarestMedal

    finalData["ranked_maps"] = user["rankedmaps"]
    finalData["loved_maps"] = user["lovedmaps"]
    finalData["replays_watched"] = user["replays"]

    finalData["avatar_url"] = user["avatar_url"]

    for key in finalData.keys():
        if finalData[key] is None:
            finalData[key] = "NULL"

    return finalData

def calculateStats(rawPP):
    stats = {}
    stats["totalpp"] = sum(rawPP)
    stats["stdevpp"] = stats["totalpp"] - 2*calculateStDevPP(rawPP)
    stats["standardpp"] = rawPP[0]
    stats["taikopp"] = rawPP[1]
    stats["ctbpp"] = rawPP[2]
    stats["maniapp"] = rawPP[3]
    return stats

def calculateStDevPP(rawPP):
    mean = sum(rawPP) / len(rawPP)
    summ = sum([pow(float(ppVal)-mean, 2) for ppVal in rawPP])
    return sqrt(summ/(len(rawPP)-1))
