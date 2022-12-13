import requests
import json

def symbol_to_name() -> dict:
    m = {}
    request = "https://api.coincap.io/v2/assets"
    response = requests.get(request)
    text = response.json()
    for i in range(0, len(text['data'])):
        symbol = str(text['data'][i]['symbol']).lower()
        id = str(text['data'][i]['id']).lower()
        m[symbol] = id
    return m

def name_to_symbol() -> dict:
    m = {}
    request = "https://api.coincap.io/v2/assets"
    response = requests.get(request)
    text = response.json()
    for i in range(0, len(text['data'])):
        symbol = str(text['data'][i]['symbol']).lower()
        id = str(text['data'][i]['id']).lower()
        m[id] = symbol
    return m

def get_list_of_crypto() -> str:
    request = "https://api.coincap.io/v2/assets"
    response = requests.get(request)
    text = response.json()
    answer = ""
    for i in range(0, len(text['data'])):
        answer += text['data'][i]['id'] + " " + text['data'][i]['symbol'] + "\n"
    return answer

def get_current_price_of_crypto(crypto: str):
    request = "https://api.coincap.io/v2/assets/" + crypto
    response = requests.get(request)
    text = response.json()
    answer = ""
    try:
        answer = str(text['data']['priceUsd']) + " " + str(text['data']['changePercent24Hr'])
    except:
        answer = "Not found"
    return answer

def best_place_to_buy_or_sell_crypto(crypto: str) -> list:
    request = "https://api.coincap.io/v2/assets/" + crypto + "/markets"
    response = requests.get(request)
    text = response.json()
    market_price_list = []
    out = []
    try:
        for i in range(0, len(text['data']), 1):
            x = []
            if (text['data'][i]['quoteSymbol'] == "USD" or text['data'][i]['quoteSymbol'] == "USDT"):
                x.append(text['data'][i]['exchangeId'])
                x.append(text['data'][i]['priceUsd'])
                market_price_list.append(x)
        sell = market_price_list[0][0]
        buy = market_price_list[0][0]
        mx = float(market_price_list[0][1])
        mn = float(market_price_list[0][1])
        for i in range(0, len(market_price_list), 1):
            if (float(market_price_list[i][1]) > mx):
                mx = float(market_price_list[i][1])
                sell = market_price_list[i][0]
            if (float(market_price_list[i][1]) < mn):
                mn = float(market_price_list[i][1])
                buy = market_price_list[i][0]
        out = [[mx, sell], [mn, buy]]
    except:
        out = ["Not found"]

    return out

def check_valid_crypto(crypto: str, symbol_from_name: dict, name_from_symbol: dict) -> bool:
    crypto = crypto.lower()
    if (crypto in symbol_from_name or crypto in name_from_symbol):
        return True
    else:
        return False
