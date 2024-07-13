import json
import boto3
import random
from botocore.exceptions import ClientError

client = boto3.client('dynamodb')

def lambda_handler(event, context):
    intent = event['currentIntent']['name']
    Accountnumber1 = event['currentIntent']['slots']['Senderacc']
    Accountnumber2 = event['currentIntent']['slots']['Receiveracc']
    amt = float(event['currentIntent']['slots']['Amount'])
    
    if intent == 'FundTransfer':
        response = fundtransfer(Accountnumber1, Accountnumber2, amt)
        return response

def fundtransfer(Accountnumber1, Accountnumber2, amt):
    table_name = 'customerdetails'
    
    # Get current balances
    balance1 = get_balance(Accountnumber1)
    balance2 = get_balance(Accountnumber2)
    
    if balance1 is None or balance2 is None:
        return balance1 if balance1 is None else balance2
    
    # Check if sufficient balance is available
    if balance1 < amt:
        message = f'Insufficient balance in account {Accountnumber1}. Transfer failed.'
        result = {
            "dialogAction": {
                "type": "Close",
                "fulfillmentState": "Failed",
                "message": {
                    "contentType": "PlainText",
                    "content": message
                }
            }
        }
        return result
    
    # Update balances
    new_balance1 = balance1 - amt
    new_balance2 = balance2 + amt
    
    # Update DynamoDB with new balances
    try:
        update_balance(Accountnumber1, new_balance1)
        update_balance(Accountnumber2, new_balance2)
        
        message = f'Successfully transferred ${amt} from account {Accountnumber1} to account {Accountnumber2}.'
        result = {
            "dialogAction": {
                "type": "Close",
                "fulfillmentState": "Fulfilled",
                "message": {
                    "contentType": "PlainText",
                    "content": message
                }
            }
        }
        return result
    
    except ClientError as e:
        error_message = e.response['Error']['Message']
        result = {
            "dialogAction": {
                "type": "Close",
                "fulfillmentState": "Failed",
                "message": {
                    "contentType": "PlainText",
                    "content": f'Failed to transfer funds. Error: {error_message}'
                }
            }
        }
        return result

def get_balance(Accountnumber):
    try:
        response = client.get_item(
            TableName='customerdetails',
            Key={
                'accountnumber': {'S': Accountnumber}
            }
        )
        if 'Item' in response:
            balance = float(response['Item']['balance']['N'])
            return balance
        else:
            message = "Sorry, I can't find your details in our records. Please contact our support center on 8083829227."
            result = {
                "dialogAction": {
                    "type": "Close",
                    "fulfillmentState": "Failed",
                    "message": {
                        "contentType": "PlainText",
                        "content": message
                    }
                }
            }
            return result
    except ClientError as e:
        error_message = e.response['Error']['Message']
        result = {
            "dialogAction": {
                "type": "Close",
                "fulfillmentState": "Failed",
                "message": {
                    "contentType": "PlainText",
                    "content": f'Error retrieving balance. Error: {error_message}'
                }
            }
        }
        return result

def update_balance(Accountnumber, new_balance):
    client.update_item(
        TableName='customerdetails',
        Key={
            'accountnumber': {'S': Accountnumber}
        },
        UpdateExpression='SET balance = :val',
        ExpressionAttributeValues={
            ':val': {'N': str(new_balance)}
        }
    )
