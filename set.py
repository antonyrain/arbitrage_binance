import json

js = open("./settings.json", "r")
set = json.load(js)
js.close()

amount = set["amount"]
greater = set["greater"]
less = set["less"]
stbCoin = set["stablecoin"]
depth = set["coinMarketCup_rank"]
rounds = set["rounds"]
timer = set["timer"]