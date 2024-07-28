#Check balance of the account number provided by the user
import json
import boto3

client = boto3.client('dynamodb')

def lambda_handler(event, context):
    intent = event['currentIntent']['name']
    slots = event['currentIntent']['slots']

    if intent == 'BalanceEnquiry':
        Accountnumber = slots['AccountNumber']
        return balanceenquiry(Accountnumber)

def balanceenquiry(Accountnumber):
    try:
        response = client.get_item(TableName='customerdetails', Key={'accountnumber': {'S': Accountnumber}})
        item = response['Item']
        balance = item['balance']['N']
        message = f'Your account balance is {balance}'
        return {
            "dialogAction": {
                "type": "Close",
                "fulfillmentState": "Fulfilled",
                "message": {
                    "contentType": "PlainText",
                    "content": message
                }
            }
        }
    except Exception as e:
        message = f'Failed to check balance. Error: {str(e)}'
        return {
            "dialogAction": {
                "type": "Close",
                "fulfillmentState": "Failed",
                "message": {
                    "contentType": "PlainText",
                    "content": message
                }
            }
        }
