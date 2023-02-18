import os
import requests
from binance.client import Client
from binance.exceptions import BinanceAPIException
from binance.websockets import BinanceSocketManager
from datetime import datetime

# Binance API credentials
BINANCE_API_KEY = os.environ.get('BINANCE_API_KEY')
BINANCE_API_SECRET = os.environ.get('BINANCE_API_SECRET')

# Binance client
client = Client(BINANCE_API_KEY, BINANCE_API_SECRET)

# Helper functions
def get_symbol(base, quote):
    symbol = base + quote
    symbols = [s['symbol'] for s in client.get_exchange_info()['symbols']]
    if symbol in symbols:
        return symbol
    else:
        return None

def calculate_profit(base, quote1, quote2, prices):
    symbol1 = get_symbol(base, quote1)
    symbol2 = get_symbol(quote1, quote2)
    symbol3 = get_symbol(quote2, base)

    if symbol1 and symbol2 and symbol3:
        price1 = prices.get(symbol1)
        price2 = prices.get(symbol2)
        price3 = prices.get(symbol3)

        if price1 and price2 and price3:
            rate1 = price1 / price2
            rate2 = rate1 * price3
            if rate2 > 1:
                return (rate2 - 1) * 100

# Base currency
base_currency = 'BTC'

# Quote currencies
quote_currencies = ['USDT', 'ETH', 'BNB', 'ADA', 'XRP', 'DOGE', 'DOT', 'SOL', 'LUNA', 'AVAX', 'LINK']

# WebSocket connection
bm = BinanceSocketManager(client)

# Dictionary to hold latest prices
prices = {}

def process_message(msg):
    symbol = msg['s']
    price = float(msg['c'])
    prices[symbol] = price

    # Calculate triangular arbitrage opportunities
    max_profit = 0
    max_profit_trade = None

    for quote1 in quote_currencies:
        for quote2 in quote_currencies:
            if quote1 != quote2:
                profit = calculate_profit(base_currency, quote1, quote2, prices)
                if profit and profit > max_profit:
                    max_profit = profit
                    max_profit_trade = (base_currency, quote1, quote2)

    if max_profit_trade:
        print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Max profit: {max_profit:.2f}%")
        print(f"Trade: {max_profit_trade[0]} -> {max_profit_trade[1]} -> {max_profit_trade[2]} -> {max_profit_trade[0]}")
    else:
        print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - No profitable trade found.")

# Subscribe to ticker updates for all symbols
conn_key = bm.start_ticker_socket(process_message)
bm.start()
