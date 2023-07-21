#!/usr/bin/env python3
from api_keys import binance_api_key, binance_api_secret
from binance.spot import Spot as SpotClient
from service import getAvgPrice, coinMarketCup
from config import amount, greater, less, stbCoin, rounds, timer
from termcolor import colored
import time

spot = SpotClient(key=binance_api_key, secret=binance_api_secret)

list = coinMarketCup()
num_assets = len(list)
print(colored("Number of assets to check: ", "blue"), num_assets)

it = 0
while it != rounds:
    counter = num_assets
    for tCoin in list:
        f = open("delta.txt", "a")
        counter -= 1
        print("_" * 44)
        print(colored(">>>>>>>>>> Check crypto coin: ", "magenta"), tCoin)
        print("_" * 44)
        f.write(f"\nCheck coin: {tCoin}")

        isEth = True
        try:
            res = spot.depth(symbol=f"{tCoin}ETH", limit=1)
            eth_btc_ask = float(res["asks"][0][0])
            eth_btc_bid = float(res["bids"][0][0])
        except:
            print(f"{tCoin}/ETH spot trading pair does not available on the binance")
            isEth = False

        isBnb = True
        try:
            res = spot.depth(symbol=f"{tCoin}BNB", limit=1)
            bnb_btc_ask = float(res["asks"][0][0])
            bnb_btc_bid = float(res["bids"][0][0])
        except:
            print(f"{tCoin}/BNB spot trading pair does not available on the binance")
            isBnb = False

        if isEth:
            triangle = 1
            btc_qty = amount / getAvgPrice(f"BTC{stbCoin}", amount, "asks")
            print(colored(f"Triangle: {triangle}", "cyan"))
            print(colored(f"Start with BTC qty: ", "magenta"), btc_qty)
            # """ Forward
            # ETH <= BTC / ask 
            # COIN <= ETH / ask
            # COIN * bid => BTC
            # """
            eth_qty = btc_qty / getAvgPrice("ETHBTC", btc_qty, "asks")
            coin_qty = eth_qty / getAvgPrice(f"{tCoin}ETH", eth_qty, "asks")
            new_btc_qty = coin_qty * getAvgPrice(f"{tCoin}BTC", coin_qty, "bids")
            print(colored("Forward: ", "yellow"), f"{new_btc_qty:.8f}")
            differ = new_btc_qty - btc_qty
            if differ > greater and differ < less:
                print(colored("Gain: ", "yellow"), colored(f"{differ:.8f}", "green"))
                f.write(f"\n{tCoin} triangle: {triangle} forward gain: {differ:.8f}")
            else:
                print(colored("Loss: ", "yellow"), colored(f"{differ:.8f}", "red"))
            
            # """ Reverse
            # COIN <= BTC / ask
            # COIN * bid => ETH
            # ETH * bid => BTC
            # """
            coin_qty = btc_qty / getAvgPrice(f"{tCoin}BTC", btc_qty, "asks")
            eth_qty = coin_qty * getAvgPrice(f"{tCoin}ETH", coin_qty, "bids")
            new_btc_qty = eth_qty * getAvgPrice("ETHBTC", eth_qty, "bids")
            print(colored("Reverse: ", "yellow"), new_btc_qty)
            differ = new_btc_qty - btc_qty
            if differ > greater and differ < less: 
                print(colored("Gain: ", "yellow"), colored(f"{differ:.8f}", "green"))
                f.write(f"\n{tCoin} triangle: {triangle} reverse gain: {differ:.8f}")
            else:
                print(colored("Loss: ", "yellow"), colored(f"{differ:.8f}", "red"))

        if isBnb:
            triangle = 2
            btc_qty = amount / getAvgPrice(f"BTC{stbCoin}", amount, "asks")
            print(colored(f"Triangle: {triangle}", "cyan"))
            print(colored("Start with BTC qty: ", "magenta"), btc_qty)
            # """ Forward
            # BNB <= BTC / ask
            # COIN <= BNB / ask
            # COIN * bid => BTC
            # """
            bnb_qty = btc_qty / getAvgPrice("BNBBTC", btc_qty, "asks")
            coin_qty = bnb_qty / getAvgPrice(f"{tCoin}BNB", bnb_qty, "asks")
            new_btc_qty = coin_qty * getAvgPrice(f"{tCoin}BTC", coin_qty, "bids")
            print(colored("Forward: ", "yellow"), new_btc_qty)
            differ = new_btc_qty - btc_qty
            if differ > greater and differ < less:
                print(colored("Gain: ", "yellow"), colored(f"{differ:.8f}", "green"))
                f.write(f"\n{tCoin} triangle: {triangle} forward gain: {differ:.8f}")
            else:
                print(colored("Loss: ", "yellow"), colored(f"{differ:.8f}", "red"))

            # """ Reverse
            # COIN <= BTC / ask
            # COIN * bid => BNB
            # BNB * bid => BTC
            # """
            coin_qty = btc_qty / getAvgPrice(f"{tCoin}BTC", btc_qty, "asks")
            bnb_qty = coin_qty * getAvgPrice(f"{tCoin}BNB", coin_qty, "bids")
            new_btc_qty = bnb_qty * getAvgPrice("BNBBTC", bnb_qty, "bids")
            print(colored("Reverse: ", "yellow"), new_btc_qty)
            differ = new_btc_qty - btc_qty
            if differ > greater and differ < less:
                print(colored("Gain: ", "yellow"), colored(f"{differ:.8f}", "green"))
                f.write(f"\n{tCoin} triangle: {triangle} reverse gain: {differ:.8f}")
            else:
                print(colored("Loss: ", "yellow"), colored(f"{differ:.8f}", "red"))

        if isEth:
            triangle = 3
            eth_qty = amount / getAvgPrice(f"ETH{stbCoin}", amount, "asks")
            print(colored(f"Triangle: {triangle}", "cyan"))
            print(colored("Start with ETH qty: ", "magenta"), eth_qty)
            # """ Forward
            # ETH * bid => BTC
            # COIN <= BTC / ask
            # COIN * bid => ETH
            # """
            btc_qty = eth_qty * getAvgPrice(f"ETHBTC", eth_qty, "bids")
            coin_qty = btc_qty / getAvgPrice(f"{tCoin}BTC", btc_qty, "asks")
            new_eth_qty = coin_qty * getAvgPrice(f"{tCoin}ETH", coin_qty, "bids")
            print(colored("Forward: ", "yellow"), new_eth_qty)
            differ = new_eth_qty - eth_qty
            if differ > greater and differ < less: 
                print(colored("Gain: ", "yellow"), colored(f"{differ:.8f}", "green"))
                f.write(f"\n{tCoin} triangle: {triangle} forward gain: {differ:.8f}")
            else:
                print(colored("Loss: ", "yellow"), colored(f"{differ:.8f}", "red"))
            
            # """ Reverse
            # COIN <= ETH / ask
            # COIN * bid => BTC
            # ETH <= BTC / ask
            # """
            coin_qty = eth_qty / getAvgPrice(f"{tCoin}ETH", eth_qty, "asks")
            bts_qty = coin_qty * getAvgPrice(f"{tCoin}BTC", coin_qty, "bids")
            new_eth_qty = btc_qty / getAvgPrice(f"ETHBTC", btc_qty, "asks")
            print(colored("Reverse: ", "yellow"), new_eth_qty)
            differ = new_eth_qty - eth_qty
            if differ > greater and differ < less:
                print(colored("Gain: ", "yellow"), colored(f"{differ:.8f}", "green"))
                f.write(f"\n{tCoin} triangle: {triangle} reverse gain: {differ:.8f}")
            else:
                print(colored("Loss: ", "yellow"), colored(f"{differ:.8f}", "red"))

        if isBnb:
            triangle = 4
            bnb_qty = amount / getAvgPrice(f"BNB{stbCoin}", amount, "asks")
            print(colored(f"Triangle: {triangle}", "cyan"))
            print(colored("Start with BNB qty: ", "magenta"), bnb_qty)
            # """ Forward
            # BNB * bid => BTC
            # COIN <= BTC / ask
            # COIN * bid => BNB
            # """
            btc_qty = bnb_qty * getAvgPrice(f"BNBBTC", bnb_qty, "bids")
            coin_qty = btc_qty / getAvgPrice(f"{tCoin}BTC", btc_qty, "asks")
            new_bnb_qty = coin_qty * getAvgPrice(f"{tCoin}BNB", coin_qty, "bids")
            print(colored("Forward: ", "yellow"), new_bnb_qty)
            differ = new_bnb_qty - bnb_qty
            if differ > greater and differ < less:
                print(colored(f"Gain: ", "yellow"), colored(f"{differ:.8f}", "green"))
                f.write(f"\n{tCoin} triangle: {triangle} forward gain: {differ:.8f}")
            else:
                print(colored("Loss: ", "yellow"), colored(f"{differ:.8f}", "red"))

            # """ Reverse
            # COIN <= BNB / ask
            # COIN * bid => BTC
            # BNB <= BTC / ask
            # """
            coin_qty = bnb_qty / getAvgPrice(f"{tCoin}BNB", bnb_qty, "asks")
            btc_qty = coin_qty * getAvgPrice(f"{tCoin}BTC", coin_qty, "bids")
            new_bnb_qty = btc_qty / getAvgPrice(f"BNBBTC", btc_qty, "asks")
            print(colored("Reverse: ", "yellow"), new_bnb_qty)
            differ = new_bnb_qty - bnb_qty
            if differ > greater and differ < less:
                print(colored(f"Gain: ", "yellow"), colored(f"{differ:.8f}", "green"))
                f.write(f"\n{tCoin} triangle:{triangle} reverse gain: {differ:.8f}")
            else:
                print(colored("Loss: ", "yellow"), colored(f"{differ:.8f}", "red"))
        
        if isEth and isBnb:
            triangle = 5
            eth_qty = amount / getAvgPrice(f"ETH{stbCoin}", amount, "asks")
            print(colored(f"Triangle: {triangle}", "cyan"))
            print(colored("Start with ETH qty: ", "magenta"), eth_qty)
            # """ Forward
            # BNB <= ETH / ask 
            # COIN <= BNB / ask
            # COIN * bid => ETH
            # """
            bnb_qty = eth_qty / getAvgPrice(f"BNBETH", eth_qty, "asks")
            coin_qty = bnb_qty / getAvgPrice(f"{tCoin}BNB", bnb_qty, "asks")
            new_eth_qty = coin_qty * getAvgPrice(f"{tCoin}ETH", coin_qty, "bids")
            print(colored("Forward: ", "yellow"), new_eth_qty)
            differ = new_eth_qty - eth_qty
            if differ > greater and differ < less:
                print(colored("Gain: ", "yellow"), colored(f"{differ:.8f}", "green"))
                f.write(f"\n{tCoin} triangle: {triangle} forward gain: {differ:.8f}")
            else:
                print(colored("Loss: ", "yellow"), colored(f"{differ:.8f}", "red"))

            # """ Reverse
            # COIN <= ETH / ask 
            # COIN * bid => BNB
            # BNB * bid => ETH
            # """
            coin_qty = eth_qty / getAvgPrice(f"{tCoin}ETH", eth_qty, "asks")
            bnb_qty = coin_qty * getAvgPrice(f"{tCoin}BNB", coin_qty, "bids")
            new_eth_qty = bnb_qty * getAvgPrice(f"BNBETH", bnb_qty, "bids")
            print(colored("Reverse: ", "yellow"), new_eth_qty)
            differ = new_eth_qty - eth_qty
            if differ > greater and differ < less:
                print(colored(f"Gain: ", "yellow"), colored(f"{differ:.8f}", "green"))
                f.write(f"\n{tCoin} triangle: {triangle} reverse gain: {differ:.8f}")
            else:
                print(colored("Loss: ", "yellow"), colored(f"{differ:.8f}", "red"))
            
        if isEth and isBnb:
            triangle = 6
            bnb_qty = amount / getAvgPrice(f"BNB{stbCoin}", amount, "asks")
            print(colored(f"Triangle: {triangle} ", "cyan"))
            print(colored("Start with BNB qty: ", "magenta"), bnb_qty)
            # """ Forward
            # BNB * bid => ETH
            # COIN <= ETH / ask
            # COIN * bid => BNB
            # """
            eth_qty = bnb_qty * getAvgPrice(f"BNBETH", bnb_qty, "bids")
            coin_qty = eth_qty / getAvgPrice(f"{tCoin}ETH", eth_qty, "asks")
            new_bnb_qty = coin_qty * getAvgPrice(f"{tCoin}BNB", coin_qty, "bids")
            print(colored("Forward: ", "yellow"), new_bnb_qty)
            differ = new_bnb_qty - bnb_qty
            if differ > greater and differ < less:
                print(colored("Gain: ", "yellow"), colored(f"{differ:.8f}", "green"))
                f.write(f"\n{tCoin} triangle: {triangle} forward gain: {differ:.8f}")
            else:
                print(colored("Loss: ", "yellow"), colored(f"{differ:.8f}", "red"))

            # """ Reverse
            # COIN <= BNB / ask
            # COIN * bid => ETH
            # BNB <= ETH / ask
            # """
            coin_qty = bnb_qty / getAvgPrice(f"{tCoin}BNB", bnb_qty, "asks")
            eth_qty = coin_qty * getAvgPrice(f"{tCoin}ETH", coin_qty, "bids")
            new_bnb_qty = eth_qty / getAvgPrice(f"BNBETH", eth_qty, "asks")
            print(colored("Reverse: ", "yellow"), new_bnb_qty)
            differ = new_bnb_qty - bnb_qty
            if differ > greater and differ < less:
                print(colored("Gain: ", "yellow"), colored(f"{differ:.8f}", "green"))
                f.write(f"\n{tCoin} triangle: {triangle} reverse gain: {differ:.8f}")
            else:
                print(colored("Loss: ", "yellow"), colored(f"{differ:.8f}", "red"))
        

        if isBnb:
            triangle = 7
            coin_qty = amount / getAvgPrice(f"{tCoin}{stbCoin}", amount, "asks")
            print(colored(f"Triangle: {triangle}", "cyan"))
            print(colored(f"Start with {tCoin} qty: ", "magenta"), coin_qty)
            # """ Forward
            # COIN * bid => BTC
            # BNB <= BTC / ask
            # COIN <= BNB / ask
            # """
            btc_qty = coin_qty * getAvgPrice(f"{tCoin}BTC", coin_qty, "bids")
            bnb_qty = btc_qty / getAvgPrice(f"BNBBTC", btc_qty, "asks")
            new_coin_qty = bnb_qty / getAvgPrice(f"{tCoin}BNB", bnb_qty, "asks")
            print(colored("Forward: ", "yellow"), new_coin_qty)
            differ = new_coin_qty - coin_qty
            if differ > greater and differ < less:
                print(colored(f"Gain: ", "yellow"), colored(f"{differ:.8f}", "green"))
                f.write(f"\n{tCoin} triangle: {triangle} forward gain: {differ:.8f}")
            else:
                print(colored("Loss: ", "yellow"), colored(f"{differ:.8f}", "red"))

            # """ Reverse
            # COIN * bid => BNB
            # BNB * bid => BTC
            # COIN <= BTC / ask
            # """
            bnb_qty = coin_qty * getAvgPrice(f"{tCoin}BNB", coin_qty, "bids")
            btc_qty = bnb_qty * getAvgPrice(f"BNBBTC", bnb_qty, "bids")
            new_coin_qty = btc_qty / getAvgPrice(f"{tCoin}BTC", btc_qty, "asks")
            print(colored("Reverse: ", "yellow"), new_coin_qty)
            differ = new_coin_qty - coin_qty
            if differ > greater and differ < less:
                print(colored("Gain: ", "yellow"), colored(f"{differ:.8f}", "green"))
                f.write(f"\n{tCoin} triangle: {triangle} reverse gain: {differ:.8f}")
            else:
                print(colored("Loss: ", "yellow"), colored(f"{differ:.8f}", "red"))

        if isEth:
            triangle = 8
            coin_qty = amount / getAvgPrice(f"{tCoin}{stbCoin}", amount, "asks")
            print(colored(f"Triangle: {triangle}", "cyan"))
            print(colored(f"Start with {tCoin} qty: ", "magenta"), coin_qty)
            # """ Forward
            # COIN * bid => BTC
            # ETH <= BTC / ask
            # COIN <= ETH / ask
            # """
            btc_qty = coin_qty * getAvgPrice(f"{tCoin}BTC", coin_qty, "bids")
            eth_qty = btc_qty / getAvgPrice(f"ETHBTC", btc_qty, "asks")
            new_coin_qty = eth_qty / getAvgPrice(f"{tCoin}ETH", eth_qty, "asks")
            print(colored("Forward: ", "yellow"), new_coin_qty)
            differ = new_coin_qty - coin_qty
            if differ > greater and differ < less:
                print(colored("Gain: ", "yellow"), colored(f"{differ:.8f}", "green"))
                f.write(f"\n{tCoin} triangle: {triangle} forward gain: {differ:.8f}")
            else:
                print(colored("Loss: ", "yellow"), colored(f"{differ:.8f}", "red"))

            # """ Reverse
            # COIN * bid => ETH
            # ETH *bid => BTC
            # COIN <= BTC / ask
            # """
            eth_qty = coin_qty * getAvgPrice(f"{tCoin}ETH", coin_qty, "bids")
            btc_qty = eth_qty * getAvgPrice(f"ETHBTC", eth_qty, "bids")
            new_coin_qty = btc_qty / getAvgPrice(f"{tCoin}BTC", btc_qty, "asks")
            print(colored("Reverse: ", "yellow"), new_coin_qty)
            differ = new_coin_qty - coin_qty
            if differ > greater and differ < less:
                print(colored("Gain: ", "yellow"), colored(f"{differ:.8f}", "green"))
                f.write(f"\n{tCoin} triangle: {triangle} reverse gain: {differ:.8f}")
            else:
                print(colored("Loss: ", "yellow"), colored(f"{differ:.8f}", "red"))

        if isEth and isBnb:
            triangle = 9
            coin_qty = amount / getAvgPrice(f"{tCoin}{stbCoin}", amount, "asks")
            print(colored(f"Triangle: {triangle}", "cyan"))
            print(colored(f"Start with {tCoin} qty: ", "magenta"), coin_qty)
            # """ Forward
            # COIN * bid => ETH
            # BNB <= ETH / ask
            # COIN <= BNB / ask
            # """
            eth_qty = coin_qty * getAvgPrice(f"{tCoin}ETH", coin_qty, "bids")
            bnb_qty = eth_qty / getAvgPrice(f"BNBETH", eth_qty, "asks")
            new_coin_qty = bnb_qty / getAvgPrice(f"{tCoin}BNB", bnb_qty, "asks")
            print(colored("Forward: ", "yellow"), new_coin_qty)
            differ = new_coin_qty - coin_qty
            if differ > greater and differ < less:
                print(colored(f"Gain: ", "yellow"), colored(f"{differ:.8f}", "green"))
                f.write(f"\n{tCoin} triangle: {triangle} forward gain: {differ:.8f}")
            else:
                print(colored("Loss: ", "yellow"), colored(f"{differ:.8f}", "red"))

            # """ Reverse
            # COIN * bid => BNB
            # BNB * bid => ETH
            # COIN <= ETH / ask
            # """
            bnb_qty = coin_qty * getAvgPrice(f"{tCoin}BNB", coin_qty, "bids")
            eth_qty = bnb_qty * getAvgPrice(f"BNBETH", bnb_qty, "bids")
            new_coin_qty = eth_qty / getAvgPrice(f"{tCoin}ETH", eth_qty, "asks")
            print(colored("Reverse: ", "yellow"), new_coin_qty)
            differ = new_coin_qty - coin_qty
            if differ > greater and differ < less:
                print(colored("Gain: ", "yellow"), colored(f"{differ:.8f}", "green"))
                f.write(f"\n{tCoin} triangle: {triangle} reverce gain: {differ:.8f}")
            else:
                print(colored("Loss: ", "yellow"), colored(f"{differ:.8f}", "red"))

        if isEth:
            triangle = 10
            coin_qty = amount / getAvgPrice(f"{tCoin}{stbCoin}", amount, "asks")
            print(colored(f"Triangle: {triangle}", "cyan"))
            print(colored(f"Start with {tCoin} qty: ", "magenta"), coin_qty)
            # """ Forward
            # COIN * bid => ETH
            # ETH * bid => BTC
            # COIN <= BTC / ask
            # """
            eth_qty = coin_qty * getAvgPrice(f"{tCoin}ETH", coin_qty, "bids")
            btc_qty = eth_qty * getAvgPrice(f"ETHBTC", eth_qty, "bids")
            new_coin_qty = btc_qty / getAvgPrice(f"{tCoin}BTC", btc_qty, "asks")
            print(colored("Forward: ", "yellow"), new_coin_qty)
            differ = new_coin_qty - coin_qty
            if differ > greater and differ < less:
                print(colored("Gain: ", "yellow"), colored(f"{differ:.8f}", "green"))
                f.write(f"\n{tCoin} triangle: {triangle} forward gain: {differ:.8f}")
            else:
                print(colored("Loss: ", "yellow"), colored(f"{differ:.8f}", "red"))

            # """ Reverse
            # COIN * bid => BTC
            # ETH <= BTC / ask
            # COIN <= ETH / ask
            # """
            btc_qty = coin_qty * getAvgPrice(f"{tCoin}BTC", coin_qty, "bids")
            eth_qty = btc_qty / getAvgPrice(f"ETHBTC", btc_qty, "asks")
            new_coin_qty = eth_qty / getAvgPrice(f"{tCoin}ETH", eth_qty, "asks")
            print(colored("Reverse: ", "yellow"), new_coin_qty)
            differ = new_coin_qty - coin_qty
            if differ > greater and differ < less:
                print(colored("Gain: ", "yellow"), colored(f"{differ:.8f}", "green"))
                f.write(f"\n{tCoin} triangle: {triangle} reverse gain: {differ:.8f}")
            else:
                print(colored("Loss: ", "yellow"), colored(f"{differ:.8f}", "red"))

        if isBnb:
            triangle = 11
            coin_qty = amount / getAvgPrice(f"{tCoin}{stbCoin}", amount, "asks")
            print(colored(f"Triangle: {triangle}", "cyan"))
            print(colored(f"Start with {tCoin} qty: ", "magenta"), coin_qty)
            # """ Forward
            # COIN * bid => BNB
            # BNB * bid => BTC
            # COIN <= BTC / ask
            # """
            bnb_qty = coin_qty * getAvgPrice(f"{tCoin}BNB", coin_qty, "bids")
            btc_qty = bnb_qty * getAvgPrice(f"BNBBTC", bnb_qty, "bids")
            new_coin_qty = btc_qty / getAvgPrice(f"{tCoin}BTC", btc_qty, "asks")
            print(colored("Forward: ", "yellow"), new_coin_qty)
            differ = new_coin_qty - coin_qty
            if differ > greater and differ < less:
                print(colored("Gain: ", "yellow"), colored(f"{differ:.8f}", "green"))
                f.write(f"\n{tCoin} triangle: {triangle} forward gain: {differ:.8f}")
            else:
                print(colored("Loss: ", "yellow"), colored(f"{differ:.8f}", "red"))

            # """ Reverse
            # COIN * bid => BTC
            # BNB <= BTC / ask
            # COIN <= BNB / ask
            # """
            btc_qty = coin_qty * getAvgPrice(f"{tCoin}BTC", coin_qty, "bids")
            bnb_qty = btc_qty / getAvgPrice(f"BNBBTC", btc_qty, "asks")
            new_coin_qty = bnb_qty / getAvgPrice(f"{tCoin}BNB", bnb_qty, "asks")
            print(colored("Reverse: ", "yellow"), new_coin_qty)
            differ = new_coin_qty - coin_qty
            if differ > greater and differ < less:
                print(colored("Gain: ", "yellow"), colored(f"{differ:.8f}", "green"))
                f.write(f"\n{tCoin} triangle: {triangle} reverse gain: {differ:.8f}")
            else:
                print(colored("Loss: ", "yellow"), colored(f"{differ:.8f}", "red"))

        if isEth and isBnb:
            triangle = 12
            coin_qty = amount / getAvgPrice(f"{tCoin}{stbCoin}", amount, "asks")
            print(colored(f"Triangle: {triangle}", "cyan"))
            print(colored(f"Start with {tCoin} qty: ", "magenta"), coin_qty)
            # """ Forward
            # COIN * bid => BNB
            # BNB * bid => ETH 
            # COIN <= ETH / ask
            # """
            bnb_qty = coin_qty * getAvgPrice(f"{tCoin}BNB", coin_qty, "bids")
            eth_qty = bnb_qty * getAvgPrice(f"BNBETH", bnb_qty, "bids")
            new_coin_qty = eth_qty / getAvgPrice(f"{tCoin}ETH", eth_qty, "asks")
            print(colored("Forward: ", "yellow"), new_coin_qty)
            differ = new_coin_qty - coin_qty
            if differ > greater and differ < less:
                print(colored("Gain: ", "yellow"), colored(f"{differ:.8f}", "green"))
                f.write(f"\n{tCoin} triangle: {triangle} forward gain: {differ:.8f}")
            else:
                print(colored("Loss: ", "yellow"), colored(f"{differ:.8f}", "red"))

            # """ Reverse
            # COIN *bid => ETH
            # BNB <= ETH / ask
            # COIN <= BNB / ask
            # """
            eth_qty = coin_qty * getAvgPrice(f"{tCoin}ETH", coin_qty, "bids")
            bnb_qty = eth_qty / getAvgPrice(f"BNBETH", eth_qty, "asks")
            new_coin_qty = bnb_qty / getAvgPrice(f"{tCoin}BNB", bnb_qty, "asks")
            print(colored("Reverse: ", "yellow"), new_coin_qty)
            differ = new_coin_qty - coin_qty
            if differ > greater and differ < less:
                print(colored("Gain: ", "yellow"), colored(f"{differ:.8f}", "green"))
                f.write(f"\n{tCoin} triangle: {triangle} reverse gain: {differ:.8f}")
            else:
                print(colored("Loss: ", "yellow"), colored(f"{differ:.8f}", "red"))

        time.sleep(timer)

    print("\n")
    print(f"Round {it+1} is done!")
    print("\n")
    f.write(f"\nRound {it+1} is done!")
    f.close()
    it += 1