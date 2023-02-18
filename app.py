import os
import time
import requests
import numpy as np
from datetime import datetime
from binance.client import Client
from binance.exceptions import BinanceAPIException

# Binance API credentials
BINANCE_API_KEY = os.environ.get('BINANCE_API_KEY')
BINANCE_API_SECRET = os.environ.get('BINANCE_API_SECRET')

# Binance client
client = Client(BINANCE_API_KEY, BINANCE_API_SECRET)

# Helper functions
def get_price(symbol):
    try:
        ticker = client.get_ticker(symbol=symbol)
        price = float(ticker['lastPrice'])
        return price
    except BinanceAPIException as e:
        print(e)
        return None

def get_symbol(base, quote):
    symbol = base + quote
    symbols = [s['symbol'] for s in client.get_exchange_info()['symbols']]
    if symbol in symbols:
        return symbol
    else:
        return None

def calculate_profit(base, quote1, quote2):
    symbol1 = get_symbol(base, quote1)
    symbol2 = get_symbol(quote1, quote2)
    symbol3 = get_symbol(quote2, base)

    if symbol1 and symbol2 and symbol3:
        price1 = get_price(symbol1)
        price2 = get_price(symbol2)
        price3 = get_price(symbol3)

        if price1 and price2 and price3:
            rate1 = price1 / price2
            rate2 = rate1 * price3
            if rate2 > 1:
                return (rate2 - 1) * 100

# Base currency
base_currency = 'BTC'

# Quote currencies
quote_currencies = ['USDT', 'ETH', 'BNB', 'ADA', 'XRP', 'DOGE', 'DOT', 'SOL', 'LUNA', 'AVAX', 'LINK']

# Triangular arbitrage
max_profit = 0
max_profit_trade = None

for quote1 in quote_currencies:
    for quote2 in quote_currencies:
        if quote1 != quote2:
            profit = calculate_profit(base_currency, quote1, quote2)
            if profit and profit > max_profit:
                max_profit = profit
                max_profit_trade = (base_currency, quote1, quote2)

if max_profit_trade:
    print(f"Max profit: {max_profit:.2f}%")
    print(f"Trade: {max_profit_trade[0]} -> {max_profit_trade[1]} -> {max_profit_trade[2]} -> {max_profit_trade[0]}")
else:
    print("No profitable trade found.")
