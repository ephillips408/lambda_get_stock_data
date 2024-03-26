import json
import os

from utils import (get_stock_data, clean_stock_data)

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

    api_response = get_stock_data(
        api_key = os.environ['ALPHAVANTAGE_API_KEY'],
        symbols = ['IBM']
    )
    
    clean_data = clean_stock_data(
        data = api_response
    )

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": clean_data
            # "location": ip.text.replace("\n", "")
        }),
    }
