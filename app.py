import ccxt
import numpy as np
import pandas as pd
import time

# Define Binance API credentials
binance = ccxt.binance({
    'apiKey': 'vpKO1DecEFexXzX5gsfG8WEmHuH5DPeV4lYqFKBJGwmjeVoWwXMZjU4UFcqQFaba',
    'secret': 'mnpTkA1KNYiDBpoUsiUjQGY3KUtPOxJHcad0aFVbvSF8h5imxhAaAcriP99oiMIi',
})

# Get all available coins in Binance
symbols = binance.load_markets().keys()
coins = set([symbol.split('/')[0] for symbol in symbols] + [symbol.split('/')[1] for symbol in symbols])

# Define the amount of each currency you want to use for trading
amount = 0.1

# Define a function to calculate the profit potential for each triangular arbitrage opportunity
def calculate_profit(symbols, amount):
    ticker1 = binance.fetch_ticker(symbols[0])
    ticker2 = binance.fetch_ticker(symbols[1])
    ticker3 = binance.fetch_ticker(symbols[2])
    price1 = ticker1['bid']
    price2 = ticker2['bid'] / ticker1['ask']
    price3 = ticker3['ask'] / ticker2['ask']
    profit = (price3 * price2 * price1 * amount) - amount
    profit_percentage = (profit / amount) * 100
    return profit_percentage

# Define a function to check for triangular arbitrage opportunities
def check_triangular_arbitrage(symbols, amount):
    opportunities = []
    for i in range(len(symbols)):
        for j in range(i+1, len(symbols)):
            for k in range(j+1, len(symbols)):
                triangle = [symbols[i], symbols[j], symbols[k]]
                profit = calculate_profit(triangle, amount)
                if profit > 0:
                    opportunities.append((triangle, profit))
    return opportunities

# Continuously scan for arbitrage opportunities and display them in real-time
while True:
    for coin in coins:
        symbols = [symbol for symbol in binance.symbols if symbol.startswith(coin+'/')]
        if len(symbols) >= 3:
            opportunities = check_triangular_arbitrage(symbols, amount)
            if opportunities:
                print('Arbitrage opportunities for', coin.upper())
                for triangle, profit in opportunities:
                    print(triangle[0], '->', triangle[1], '->', triangle[2], ':', round(profit, 2), '%')
    time.sleep(1)
