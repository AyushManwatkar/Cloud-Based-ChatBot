import json
import boto3
import random
from botocore.exceptions import ClientError

client = boto3.client('dynamodb')

def lambda_handler(event, context):
    intent = event['currentIntent']['name']
    Accountnumber = event['currentIntent']['slots']['AccountNumber']
    Withdrawamt = float(event['currentIntent']['slots']['Withdrawamt'])
    
    if intent == 'Withdraw':
        response = withdraw(Accountnumber,Withdrawamt)
        return response

def withdraw(Accountnumber,Withdrawamt):
    table_name = 'customerdetails'
    
    # Get current balances
    balance = get_balance(Accountnumber)
        
    # Check if sufficient balance is available
    if balance < Withdrawamt:
        message = f'Insufficient balance in account {Accountnumber}. Withdraw Failed.'
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
    new_balance = balance-Withdrawamt    
    # Update DynamoDB with new balances
    try:
        update_balance(Accountnumber,new_balance)
        
        message = f'Successfully withdrawn ${Withdrawamt} from account {Accountnumber}.'
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
                    "content": f'Failed to withdraw. Error: {error_message}'
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
