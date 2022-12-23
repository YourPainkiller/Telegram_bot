import requests
import json

def symbol_to_name() -> dict:
    """Функция создает словарь, где ключ это сокращенное название криптовалюты, а значение название криптовалюты.
    На вход ничего не принимает. 
    return - словарь"""
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
    """Функция создает словарь, где ключ это название криптовалюты, а значение сокращенное название криптовалюты.
    На вход ничего не принимает. 
    return - словарь"""
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
    """Функция возвращает строку с всеми доступными назавниями криптовалюты для взаимодействия.
    На вход ничего не принимает.
    return - string"""
    request = "https://api.coincap.io/v2/assets"
    response = requests.get(request)
    text = response.json()
    answer = ""
    for i in range(0, len(text['data'])):
        answer += text['data'][i]['id'] + " " + text['data'][i]['symbol'] + "\n"
    return answer

def get_current_price_of_crypto(crypto: str):
    """Функция вывод цену криптовалюты crypto и ее изменение в процентах за 24 часа.
    На вход принимает строку - название криптовалюты для которой нужно узнать цену.
    return - string"""
    crypto = crypto.lower()
    answer = ""
    if check_valid_crypto(crypto, symbol_from_name, name_from_symbol):
        if crypto in name_from_symbol:
            crypto = name_from_symbol[crypto]
        request = "https://api.coincap.io/v2/assets/" + crypto
        response = requests.get(request)
        text = response.json()
        answer = str(text['data']['priceUsd']) + " " + str(text['data']['changePercent24Hr'])
    else:
        answer = "Not found"
    return answer

def best_place_to_buy_or_sell_crypto(crypto: str) -> list:
    """Функция возвращает отсортированный по возрастанию цены массив, которой состоит из [название биржи][цена] для оптимальной покупки или продажи определенной криптовалюты
    На вход принимает строку - название криптовалюты для которой нужно найти оптимальное место покупки/продажи.
    return list[][]"""
    crypto = crypto.lower()
    market_price_list = []
    if check_valid_crypto(crypto, symbol_from_name, name_from_symbol):
        if crypto in name_from_symbol:
            crypto = name_from_symbol[crypto]
        request = "https://api.coincap.io/v2/assets/" + crypto + "/markets"
        response = requests.get(request)
        text = response.json()
    
        out = []
        for i in range(0, len(text['data']), 1):
            x = []
            if (text['data'][i]['quoteSymbol'] == "USD" or text['data'][i]['quoteSymbol'] == "USDT"):
                x.append(text['data'][i]['exchangeId'])
                x.append(text['data'][i]['priceUsd'])
                market_price_list.append(x)
        market_price_list.sort(key = lambda x: x[1])
    return market_price_list

def check_valid_crypto(crypto: str, symbol_from_name: dict, name_from_symbol: dict) -> bool:
    """Функция проверяет валидность написания введенной криптовалюты.
    На вход принимает название криптовалюты и два словаря с кратким значением криптовалюты и полным названием криптовалюты.
    return bool"""
    crypto = crypto.lower()
    if (crypto in symbol_from_name or crypto in name_from_symbol):
        return True
    else:
        return False

symbol_from_name = name_to_symbol()
name_from_symbol = symbol_to_name()
