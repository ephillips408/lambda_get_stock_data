import requests
import json

def get_stock_data(api_key: str, symbols: list) -> dict:
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

  results_dict = {}

  for symbol in symbols:

    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}'
    response = requests.get(url)
    json_data = json.loads(response.text)

    results_dict[symbol] = json_data['Time Series (Daily)']

    return results_dict

def clean_stock_data(data: dict) -> list:
  """
  Takes the data returned from the `get_stock_data` and cleans it in a format that is suitable for upload to DynamoDB.
  
  Parameters
  ----------
  The dictionary that results from running `get_stock_data`
  
  Returns
  -------
  The data necessary from the API call for uploading to DynamoDB in a clean format.
  """
  
  entries = []
  
  # The keys represent each stock symbol
  for key in data.keys():
    
    # The stock data for each date returned from the API call
    for stock_data in data[key]:
      
      entries.append(
        {
          'pk': f'{key} {str(stock_data)}', # The Primary Key, example: IBM 2024-03-26
          'symbol': key,
          'date': str(stock_data),
          'open_price': data[key][str(stock_data)]['1. open'], # This is how we access the opening price
          'close_price': data[key][str(stock_data)]['4. close'], # This is how we access the closing price
          'volume': data[key][str(stock_data)]['5. volume'] # This is how we access the trade volume
        }
      )
      
    return entries
    
    
    
  
  