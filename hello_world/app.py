import json
import os
import logging
import boto3

from utils import (get_stock_data, clean_stock_data, batch_write_stocks)

logger = logging.getLogger()
logger.setLevel('INFO')

def lambda_handler(event, context):
    """Sample pure Lambda function

    Parameters
    ----------
    event: dict, required
        API Gateway Lambda Proxy Input Format

        Event doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format

    context: object, required
        Lambda Context runtime methods and attributes

        Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

    Returns
    ------
    API Gateway Lambda Proxy Output Format: dict

        Return doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
    """

    # Initialize the DynamoDB table
    db_client = boto3.client('dynamodb')
    
    # Get the stock data from the API
    api_response = get_stock_data(
        api_key = os.environ['ALPHAVANTAGE_API_KEY'],
        symbols = ['AMD', 'INTC']
    )
    
    logger.info('Successfully return the data from the API')
    
    # Clean the data that was returned from the API
    clean_data = clean_stock_data(
        data = api_response
    )
    
    logger.info('Successfully cleaned the data')
    
    # Push the data to DynamoDB
    results = batch_write_stocks(
        db_client = db_client,
        table_name = os.environ['TABLE_NAME'],
        stock_data = clean_data
    )
    
    logger.info('Successfully pushed the data to DynamoDB')

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": results
            # "location": ip.text.replace("\n", "")
        }),
    }
