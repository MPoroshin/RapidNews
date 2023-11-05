import json
from datetime import datetime
from NewsLoader import loadNews
from NewsSender import sendNews
import asyncio


async def runNewsOperations():
    while True:
        await loadNews()
        await sendNews()
        await asyncio.sleep(5)


with open('ParserConfig.json', 'r+') as file:
    parserConfig = json.load(file)
    current_date = datetime.today()
    current_date_string = current_date.strftime('%a, %d %b %Y %H:%M:%S %z').strip() + " +0300"
    for key in parserConfig.keys():
        parserConfig[f"{key}"]["lastUpdate"] = current_date_string
    file.seek(0)
    file.truncate()
    json.dump(parserConfig, file)
asyncio.run(runNewsOperations())


