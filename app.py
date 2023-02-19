import ccxt
import time

# Define Binance API credentials
binance = ccxt.binance({
    'apiKey': 'vpKO1DecEFexXzX5gsfG8WEmHuH5DPeV4lYqFKBJGwmjeVoWwXMZjU4UFcqQFaba',
    'secret': 'mnpTkA1KNYiDBpoUsiUjQGY3KUtPOxJHcad0aFVbvSF8h5imxhAaAcriP99oiMIi',
})

def get_all_symbols():
    symbols = binance.load_markets()
    return list(symbols.keys())

def check_triangular_arbitrage(symbols, amount):
    opportunities = []
    for symbol1 in symbols:
        for symbol2 in symbols:
            for symbol3 in symbols:
                if symbol1 != symbol2 and symbol1 != symbol3 and symbol2 != symbol3:
                    triangle = [symbol1, symbol2, symbol3]
                    try:
                        profit = calculate_profit(triangle, amount)
                        if profit > 0:
                            opportunities.append({
                                'triangle': triangle,
                                'profit': profit
                            })
                    except ccxt.BaseError as e:
                        print(f"Error: {e}")
    return opportunities

def calculate_profit(triangle, amount):
    ticker1 = binance.fetch_ticker(triangle[0])
    ticker2 = binance.fetch_ticker(triangle[1])
    ticker3 = binance.fetch_ticker(triangle[2])
    price1 = ticker1['ask']
    price2 = ticker2['bid']
    price3 = ticker3['bid']
    if price1 == 0 or price2 == 0:
        return 0
    return amount / price1 * price2 / price3 * price1 - amount

if __name__ == '__main__':
    symbols = get_all_symbols()
    amount = 1000
    while True:
        opportunities = check_triangular_arbitrage(symbols, amount)
        if opportunities:
            for opportunity in opportunities:
                print(f"Opportunity found! {opportunity['triangle']} - Profit: {opportunity['profit']:.2f}")
        else:
            print("No opportunities found.")
        time.sleep(1)
