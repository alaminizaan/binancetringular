import requests
import json

def get_ticker_price(symbol):
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
    response = requests.get(url)
    if response.status_code == 200:
        data = json.loads(response.content)
        return float(data['price'])
    else:
        return None

def check_triangular_arbitrage(symbols):
    rates = {}
    for i in range(len(symbols)):
        for j in range(len(symbols)):
            if i != j:
                pair1 = symbols[i] + symbols[j]
                pair2 = symbols[j] + symbols[i]
                price1 = get_ticker_price(pair1)
                price2 = get_ticker_price(pair2)
                if price1 and price2:
                    rate = price1 / price2
                    rates[pair1] = rate
    for k in rates.keys():
        for i in range(len(symbols)):
            for j in range(len(symbols)):
                if i != j:
                    if k.endswith(symbols[i]) and k.startswith(symbols[j]):
                        cross_pair = symbols[i] + symbols[j]
                        if cross_pair in rates.keys():
                            if rates[k] * rates[cross_pair] > 1:
                                return True
    return False

symbols = ['BTC', 'ETH', 'LTC']
result = check_triangular_arbitrage(symbols)
print(result)
