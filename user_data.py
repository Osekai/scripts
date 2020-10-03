from leaderboard import getUsersFromLeaderboards
from user_download import getUser
from time import sleep
import php_requests as php
import calculations as calc
import config
import ast
import logger
from math import ceil
from itertools import islice
import medals


def userData(mode, quickUpdateId=[], startId=0):
    userIdList = []

    # Not in use (yet)
    if mode == "update":
        userIdList.extend(quickUpdateId)

    # Some testing, not upload
    if mode == "test":
        userIdList.append(4504101)

    # Updating top n of all existing leaderboards
    if mode == "default":
        userIdList = list(
            map(lambda x: int(x["id"]), php.DownloadData(1000, "Ranking")))
        tmp = php.DownloadData(1000, "Members")
        userIdList.extend(list(map(lambda x: int(x["id"]), tmp)))

    # Default leaderboard download including additional users
    if mode == "full":
        userIdList = list(
            set(getUsersFromLeaderboards(config.LEADERBOARD_PAGES)))
        tmp = php.DownloadData(1000, "Members")
        userIdList.extend(list(map(lambda x: int(x["id"]), tmp)))

    # Test with leaderboard download but without any uploads
    if mode == "fulltest":
        userIdList = list(set(getUsersFromLeaderboards(1)))

    logger.Log("Got user Ids: " + str(len(userIdList)))
    open("idlog.txt", "w").write(str(userIdList))

    # Using preexisting information instead of vvvv
    userData = []
    if mode == "injectfull" or mode == "inject":
        content = open("userlog.txt", "r").read()
        userData = ast.literal_eval(content)
    # Downloading information of all users
    else:
        for i, user in enumerate(userIdList[startId:]):
            try:
                userData.append(getUser(user))
                if mode == "fulltest" and i > 10:
                    break
                if i % 1000 == 0:
                    logger.Log(str(i) + " users done")
            except Exception as err:
                logger.Log(str(user) + " failed\n" + str(err))
            sleep(1)

    # Logging data in case something fails later on
    if mode == "full":
        logger.Log("Got user data: " + str(len(userData)))
        open("userlogfull.txt", "w").write(str(userData) + "\n")
    elif mode == "default":
        logger.Log("Got user data: " + str(len(userData)))
        open("userlog.txt", "w").write(str(userData) + "\n")

    # Uploading medal meta data in case there're some new ones
    logger.Log("Uploading new medal meta data")
    php.UploadData(medals.GetMedals(3357640), "Medals")

    # Calculating and uploading the new medal data
    medalRates = []
    if mode == "full" or mode == "fulltest" or mode == "injectfull":
        logger.Log("Calculating medal rates...")
        medalRates = calc.getMedalRarity(userData)
        logger.Log("Uploading medal rates...")
        if mode != "fulltest":
            php.UploadData(medalRates, "MedalRarity")

    # Downloading already existing medal rates
    if mode == "default" or mode == "test" or mode == "update" or mode == "inject":
        logger.Log("Download medal rates...")
        tmp = php.DownloadData(1000, "MedalRarity")
        medalRates = list(
            map(lambda x: {'id': int(x['id']), 'frequency': float(x['frequency'])}, tmp))

    medalRates = sorted(medalRates, key=lambda x: x["frequency"])

    logger.Log("Got medal rates: " + str(len(medalRates)))

    # Calculating and expanding existing information for upload
    finalUserData = []
    for user in userData:
        try:
            rarestMedal = calc.getRarestMedal(user, medalRates)
            ppstats = calc.calculateStats(user["pp_raw"])
            finalUserData.append(calc.combineData(user, rarestMedal, ppstats))
        except Exception as e:
            logger.Log(
                str(user["id"]) + ": calculating additional information failed " + str(e))

    # Logging final data, in case... well, just because I can
    logger.Log("Got final user data: " + str(len(finalUserData)))
    open("userlog_final.txt", "w").write(str(finalUserData) + "\n")

    uploadAtOnce = 100
    if mode is not "test" and mode is not "fulltest":
        for i in range(int(ceil(len(finalUserData)/uploadAtOnce))):
            logger.Log("Uploading " + str(i*uploadAtOnce) +
                       " to " + str(i*uploadAtOnce+uploadAtOnce))
            php.UploadData(list(islice(finalUserData, i*uploadAtOnce,
                                       i*uploadAtOnce+uploadAtOnce)), "Ranking")
