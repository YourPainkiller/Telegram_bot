from requests_f import get_current_price_of_crypto
from requests_f import best_place_to_buy_or_sell_crypto
from requests_f import check_valid_crypto
from requests_f import name_to_symbol
from requests_f import symbol_to_name

symbol_from_name = name_to_symbol()
name_from_symbol = symbol_to_name()

def test1():
    t1 = "bitcoin"
    ans1 = get_current_price_of_crypto(t1)
    if(ans1 == "Not found"): print("WA")
    elif(type(ans1) == str): print("AC")

    t2 = "btc"
    ans2 = get_current_price_of_crypto(t2)
    if(ans2 == "Not found"): print("WA")
    elif(type(ans2) == str): print("AC")

    t3 = "eTh"
    ans3 = get_current_price_of_crypto(t3)
    if(ans3 == "Not found"): print("WA")
    elif(type(ans3) == str): print("AC")

    t4 = "asdaifoefo"
    ans4 = get_current_price_of_crypto(t4)
    if(ans4 == "Not found"): print("AC")
    else: print("WA")

    t5 = "12412412312312"
    ans5 = get_current_price_of_crypto(t5)
    if(ans5 == "Not found"): print("AC")
    else: print("WA")

    t6 = "s1das##12ewed12"
    ans6 = get_current_price_of_crypto(t6)
    if(ans6 == "Not found"): print("AC")
    else: print("WA")

def test2():
    t1 = "bitcoin"
    ans1 = best_place_to_buy_or_sell_crypto(t1)
    if(len(ans1) == 0): print("WA")
    else: print("AC")

    t2 = "asdasdvef"
    ans2 = best_place_to_buy_or_sell_crypto(t2)
    if(len(ans2) == 0): print("AC")
    else: print("WA")

    t3 = "btc"
    ans3 = best_place_to_buy_or_sell_crypto(t3)
    if(len(ans3) == 0): print("WA")
    else: print("AC")

    t4 = "sad23#$5"
    ans4 = best_place_to_buy_or_sell_crypto(t4)
    if(len(ans4) == 0): print("AC")
    else: print("WA")

def test3():
    t1 = "bitcoin"
    if(check_valid_crypto(t1, symbol_from_name, name_from_symbol)): print("AC")
    else: print("WA")
    
    t2 = "btc"
    if(check_valid_crypto(t2, symbol_from_name, name_from_symbol)): print("AC")
    else: print("WA")

    t3 = "eTh"
    if(check_valid_crypto(t3, symbol_from_name, name_from_symbol)): print("AC")
    else: print("WA")

    t4 = "sadawd2"
    if(not check_valid_crypto(t4, symbol_from_name, name_from_symbol)): print("AC")
    else: print("WA")

    t5 = "LoL123412"
    if(not check_valid_crypto(t5, symbol_from_name, name_from_symbol)): print("AC")
    else: print("WA")
    t6 = "%&@#*!#("
    if(not check_valid_crypto(t6, symbol_from_name, name_from_symbol)): print("AC")
    else: print("WA")

