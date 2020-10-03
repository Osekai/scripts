from datetime import datetime
from time import sleep
import config as c
from user_data import userData
import traceback
import logger

# This is the first "big" thing I've done in python with barely prior knowledge, so I don't care if it's not perfect.
# Questions to ElectroYan#2007

schedule = ["default", "full", "default", "default", "default",
            "default", "default", "default", "default", "default", "default"]

while True:
    for action in schedule:
        logger.Log("Beginn loop: " + action)

        try:
            userData(action)
        except Exception as e:
            logger.Log(action + ": " + traceback.format_exc() + " " + str(e))

        logger.Log("Finished loop: " + action)

        sleep(c.UPDATE_SLEEP_DURATION)
