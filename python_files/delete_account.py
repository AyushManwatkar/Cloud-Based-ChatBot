import json
import boto3
from botocore.exceptions import ClientError

client = boto3.client('dynamodb')

def lambda_handler(event, context):
    # Extract parameters from the event
    account_number = event['currentIntent']['slots']['AccountNumber']
    password = event['currentIntent']['slots']['Password']
    
    # Verify account existence and password
    result = verify_account(account_number, password)
    
    # Generate response based on verification result
    if result['statusCode'] == 200:
        return {
            'dialogAction': {
                'type': 'Close',
                'fulfillmentState': 'Fulfilled',
                'message': {
                    'contentType': 'PlainText',
                    'content': 'Account deleted successfully'
                }
            }
        }
    else:
        return {
            'dialogAction': {
                'type': 'Close',
                'fulfillmentState': 'Failed',
                'message': {
                    'contentType': 'PlainText',
                    'content': result['body']
                }
            }
        }

def verify_account(account_number, password):
    table_name = 'customerdetails'
    
    try:
        # Get item from DynamoDB
        response = client.get_item(
            TableName=table_name,
            Key={
                'accountnumber': {'S': account_number}
            }
        )
        
        # Check if the item exists
        if 'Item' in response:
            item = response['Item']
            
            # Verify password
            if item.get('password', {}).get('S') == password:
                # Delete the item from the table
                client.delete_item(
                    TableName=table_name,
                    Key={
                        'accountnumber': {'S': account_number}
                    }
                )
                return {
                    'statusCode': 200,
                    'body': 'Account deleted successfully'
                }
            else:
                return {
                    'statusCode': 400,
                    'body': 'Incorrect password'
                }
        else:
            return {
                'statusCode': 400,
                'body': 'Account does not exist'
            }
    except ClientError as e:
        error_message = e.response['Error']['Message']
        return {
            'statusCode': 500,
            'body': f'Error: {error_message}'
        }
