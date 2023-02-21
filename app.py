import os
import json
import math
import httpx
from cachetools import cached, TTLCache
from flask import Flask, request, jsonify

app = Flask(__name__)

# Configure the cache to store the results of API requests for 5 seconds
cache = TTLCache(maxsize=1024, ttl=5)

# Add your Binance API key and secret to the client
api_key = "vpKO1DecEFexXzX5gsfG8WEmHuH5DPeV4lYqFKBJGwmjeVoWwXMZjU4UFcqQFaba"
api_secret = "mnpTkA1KNYiDBpoUsiUjQGY3KUtPOxJHcad0aFVbvSF8h5imxhAaAcriP99oiMIi"
client = httpx.Client(
    headers={"X-MBX-APIKEY": api_key},
    auth=httpx.BasicAuth(api_key, api_secret),
)

# Define the endpoint for the external API
API_ENDPOINT = "https://api.binance.com/api/v3/ticker/price"

# Define a helper function for making API requests and caching the results
@cached(cache)
def get_price(symbol):
    response = client.get(API_ENDPOINT, params={"symbol": symbol})
    response.raise_for_status()
    data = response.json()
    price = float(data["price"])
    return price

# Define a helper function for calculating the profit from triangular arbitrage
def calculate_profit(triangle, amount):
    # Calculate the exchange rate for each pair of currencies in the triangle
    rate1 = get_price(triangle[0] + triangle[1])
    rate2 = get_price(triangle[1] + triangle[2])
    rate3 = get_price(triangle[2] + triangle[0])

    # Calculate the profit from triangular arbitrage using the exchange rates and input amount
    try:
        profit = amount / rate1 * rate2 / rate3 * rate1 - amount
    except ZeroDivisionError:
        return None
    else:
        return profit

# Define the endpoint for checking triangular arbitrage
@app.route("/triangular-arbitrage")
def check_triangular_arbitrage():
    # Get the input parameters from the query string
    symbols = request.args.get("symbols", "").split(",")
    amount = float(request.args.get("amount", 0))

    # Check that the input parameters are valid
    if len(symbols) != 3:
        return jsonify({"error": "Exactly 3 symbols are required"}), 400
    if amount <= 0:
        return jsonify({"error": "Amount must be greater than 0"}), 400

    # Check for triangular arbitrage opportunities and calculate the potential profits
    triangles = [(symbols[0], symbols[1], symbols[2]), (symbols[1], symbols[2], symbols[0]), (symbols[2], symbols[0], symbols[1])]
    opportunities = []
    for triangle in triangles:
        try:
            profit = calculate_profit(triangle, amount)
            if profit is not None and profit > 0:
                opportunities.append({"triangle": triangle, "profit": profit})
        except httpx.HTTPError as e:
            return jsonify({"error": f"Failed to get price: {str(e)}"}), 500

    # Return the results
    if opportunities:
        return jsonify({"opportunities": opportunities})
    else:
        return jsonify({"message": "No triangular arbitrage opportunities found"})


if __name__ == "__main__":
    # Add your Binance API key and secret to the client
    api_key = "vpKO1DecEFexXzX5gsfG8WEmHuH5DPeV4lYqFKBJGwmjeVoWwXMZjU4UFcqQFaba"
    api_secret = "mnpTkA1KNYiDBpoUsiUjQGY3KUtPOxJHcad0aFVbvSF8h5imxhAaAcriP99oiMIi"
    client = httpx.Client(
        headers={"X-MBX-APIKEY": api_key},
        auth=httpx.BasicAuth(api_key, api_secret),
    )

    # Use gunicorn as the server with 4 worker processes
    num_workers = 4
    bind_address = "0.0.0.0:5000"
    os.system(f"gunicorn --bind {bind_address} --workers {num_workers} app:app")
