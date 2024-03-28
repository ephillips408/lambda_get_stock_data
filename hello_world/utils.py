import requests
import json
import logging

from botocore.exceptions import ClientError

logger = logging.getLogger()
logger.setLevel('INFO')

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
          'PutRequest': {
            'Item': {
              'pk': { 'S': f'{key} {str(stock_data)}' }, # The Primary Key, example: IBM 2024-03-26
              'symbol': { 'S': key },
              'date': { 'S': str(stock_data) },
              'open_price': { 'N': data[key][str(stock_data)]['1. open'] }, # This is how we access the opening price
              'close_price': { 'N': data[key][str(stock_data)]['4. close'] }, # This is how we access the closing price
              'volume': { 'N': data[key][str(stock_data)]['5. volume'] } # This is how we access the trade volume
            }
          }
        }
      )
      
    return entries

def batch_write_stocks(db_client, table_name: str, stock_data: list):
  """
  Takes the data returned from `clean_stock_data()` and uploads it to DynamoDB.
  
  Parameters
  ----------
  `db_client`: The DynamoDB client, aka `boto3.client('dynamodb')`
  
  `table_name`: The name of the table that will receive the data
  
  `stock_data`: The list that is returned from `clean_stock_data()`
  """
  
  try:
    
    # Make sure that we break the list down into batches of 25 for the batch_write_item operation
    sublist_size = 25
    
    sublist_data = [ stock_data[i : i + sublist_size] for i in range(0, len(stock_data), sublist_size) ]
    
    # Uploading the batches
    for batch in sublist_data:
      
      db_client.batch_write_item(
        RequestItems = {
          table_name: batch
        }
      )
        
    return 'Data successfully uploaded.'
        
  except ClientError as err:
    
    logger.error(
        "Couldn't load data into table %s. Here's why: %s: %s",
        table_name,
        err.response["Error"]["Code"],
        err.response["Error"]["Message"],
    )
    raise
