#!/bin/bash

# Set your Binance API key and secret
export BINANCE_API_KEY='vpKO1DecEFexXzX5gsfG8WEmHuH5DPeV4lYqFKBJGwmjeVoWwXMZjU4UFcqQFaba'
export BINANCE_SECRET='mnpTkA1KNYiDBpoUsiUjQGY3KUtPOxJHcad0aFVbvSF8h5imxhAaAcriP99oiMIi'

# Create the requirements.txt file
echo "python-binance" > requirements.txt

# Create the Procfile file
echo "web: python app.py" > Procfile

# Install the required dependencies
pip install -r requirements.txt

# Deploy the app to Scalingo
scalingo create my-app
scalingo env-set BINANCE_API_KEY=$BINANCE_API_KEY
scalingo env-set BINANCE_SECRET=$BINANCE_SECRET
scalingo deploy

# Open a command prompt for the app
scalingo run bash
