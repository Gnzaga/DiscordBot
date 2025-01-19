from alpha_vantage.timeseries import TimeSeries
import resources
from pprint import pprint

ts = TimeSeries(key=resources.alphaVantageKey, output_format='pandas')

from alpha_vantage.cryptocurrencies import CryptoCurrencies


crypto = CryptoCurrencies(key=resources.alphaVantageKey, output_format='pandas')
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
