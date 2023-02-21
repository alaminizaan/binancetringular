import requests

binance_url = "https://api.binance.com/api/v3/ticker/price"

response = requests.get(binance_url)

if response.status_code == 200:
    prices = response.json()
    for price in prices:
        print(f"{price['symbol']}: {price['price']}")
else:
    print("Failed to get prices from Binance API")
