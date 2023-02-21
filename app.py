import requests

# Define the API endpoint
url = "https://api.binance.com/api/v3/exchangeInfo"

# Send a GET request to the endpoint and get the response
response = requests.get(url)

# Check if the response was successful
if response.status_code == 200:
    # Get the JSON data from the response
    data = response.json()

    # Loop through all symbols and print their base and quote assets
    for symbol in data['symbols']:
        base_asset = symbol['baseAsset']
        quote_asset = symbol['quoteAsset']
        print(f"{base_asset}/{quote_asset}")
else:
    # Print an error message if the request was not successful
    print(f"Error {response.status_code}: {response.text}")
