from requests import Session
from api_keys import binance_api_key, binance_api_secret, coinMarketCup_api_key
from binance.spot import Spot as SpotClient
from config import depth
import json


spot = SpotClient(key=binance_api_key, secret=binance_api_secret)


def coinMarketCup():
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    parameters = {
        'start': '1',
        'limit': str(depth),  # should be a string type
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': coinMarketCup_api_key,
    }

    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(url, params=parameters)
        res = json.loads(response.text)
    except Exception as e:
        print(e)

    symbols_list = []
    for d in res["data"]:

        symbols_list.append(d["symbol"])

    remove_from = [
        "BUSD",
        "BTC",
        "ETH",
        "BNB",
        "USDT",
        "USDC"
    ]
    for r in remove_from:
        symbols_list.remove(r)

    return symbols_list


def getAvgPrice(symbol, amount, side):
    if side == "asks":
        res = spot.depth(symbol=symbol, limit=99)
        myQty = amount / float(res["asks"][0][0])
        sum_price_qty = 0
        count = 1
        qty = myQty
        for i in res["asks"]:
            bookPrice = float(i[0])
            bookQty = float(i[1])
            if qty < bookQty and count == 1:
                return bookPrice
            elif qty < bookQty and count != 1:
                sum_price_qty += bookPrice * qty
                break
            else:
                sum_price_qty += bookPrice * bookQty
                qty = abs(bookQty - qty)
            count +=1
        return sum_price_qty / myQty

    if side == "bids":
        res = spot.depth(symbol=symbol, limit=99)
        myQty = amount
        sum_price_qty = 0
        count = 1
        qty = myQty
        for i in res["bids"]:
            bookPrice = float(i[0])
            bookQty = float(i[1])
            if qty < bookQty and count == 1:
                return bookPrice
            elif qty < bookQty and count != 1:
                sum_price_qty += bookPrice * qty
                break
            else:
                sum_price_qty += bookPrice * bookQty
                qty = abs(bookQty - qty)
            count +=1
        return sum_price_qty / myQty

# weighted_average_price = getAvgPrice("BTCBUSD", 0.06, "asks")
# print(weighted_average_price)
