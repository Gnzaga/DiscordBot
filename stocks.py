import os
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.cryptocurrencies import CryptoCurrencies
import resources

# Get API key from environment variable or fall back to resources file
ALPHA_VANTAGE_KEY = os.getenv('ALPHA_VANTAGE_KEY', resources.alphaVantageKey)

ts = TimeSeries(key=ALPHA_VANTAGE_KEY, output_format='pandas')
crypto = CryptoCurrencies(key=ALPHA_VANTAGE_KEY, output_format='pandas')
#data['4. close']

def getLatestPrice(name):
  name = name.upper()
  try:
    stock_data, stock_meta_data = ts.get_intraday(symbol = name, interval='60min', outputsize='full')
    return stock_data['4. close'][0]

  except ValueError:
    return "Error, Incorrect Stock Symbol"



def getCrypto(symbol):
  symbol = symbol.upper()
  try:
    crypto_data, crypto_meta_data = crypto.get_digital_currency_daily(symbol=symbol,market="USD")
    return crypto_data["4a. close (USD)"][0]
  except ValueError:
    return "Error, Incorrect Crypto Symbol"
