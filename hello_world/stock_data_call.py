import requests

def get_stock_data(api_key: str, symbols: list):
  """
  Gets the stock data from the Alphavantage API for each stock symbol in the `symbols` list.

  Parameters
  ----------

  `api_key`: The Alphavantage API key that can be obtained at this link: https://www.alphavantage.co/support/#api-key

  `symbols`: A list containing the stock symbols of interest, for example `IBM`

  Returns
  -------

  A dictionary of the responses for each symbol in the `symbols` list.
  """

  for symbol in symbols:

    # replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}'
    r = requests.get(url)
    data = r.json()

    return data

