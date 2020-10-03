from datetime import datetime

def Log(message):
    print("[" + str(datetime.now()) + "] " + message + "\n")
    open("log.txt", "a").write("[" + str(datetime.now()) + "] " + message + "\n")