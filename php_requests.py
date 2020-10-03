import requests
import config as c
import json
import logger
import sql
def UploadData(data, table): #MedalRarity, Ranking, Medals
    sqls = sql.createSql(data, table)
    payload = {"api_key":c.api_key, "table": table, "data":sqls}
    r = requests.post(c.url_up, data={'value':json.dumps(payload)})
    successes = r.text
    successCount = successes.count("1")
    logger.Log("Upload "+ str(table) +": Succeeded: " + str(successCount) + "/" + str(len(sqls)))
    if (successCount < len(sqls)):
        for i in range(len(sqls)):
            if (successes[i] == "0"):
                logger.Log("Upload "+ str(table) +": Failed: " + sqls[i])


def DownloadData(count, table): #Ranking, Members, MedalRarity
    payload = {"api_key":c.api_key, "table":table, "count":count}
    r = requests.post(c.url_down, data=payload)
    logger.Log("Download "+ str(count)+ " " + table +": " + r.text[:100])
    return json.loads(r.text)