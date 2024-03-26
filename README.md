### get-stock-data

#### This is still a work in progress

This Lambda function gets stock data by calling the [Alphavantage API](https://www.alphavantage.co/documentation/), then cleaning the data as necessary, and finally pushing the cleaned data to DynamoDB. This is being tested on the local installation of DynamoDB, and more information about this service can be found [here](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/DynamoDBLocal.html).

This project was created using the [AWS SAM CLI]('https://aws.amazon.com/serverless/sam/). To build the function prior to running, use the command
  * `sam build`
in the terminal, and to run the code, use the command
  * `sam local invoke`

In order to add environment variables, first, they must be created by running the command `export SECRET_NAME=value`, and then referenced in `template.yaml` by

```yaml
Resources:
  YourFunctionName:
    Properties:
      Environment:
        Variables:
          SECRET_NAME: ${SECRET_NAME}
```