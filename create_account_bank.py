import json
import boto3
import random
from botocore.exceptions import ClientError

client = boto3.client('dynamodb')

def generate_five_digit_number():
    number = random.randint(10000, 99999)
    return str(number)

def lambda_handler(event, context):
    intent = event['currentIntent']['name']
    Accountnumber = generate_five_digit_number()
    Name = event['currentIntent']['slots']['Name']
    Creditamt = event['currentIntent']['slots']['CreditAmount']
    Contactnum = event['currentIntent']['slots']['ContactNumber']
    
    if intent == 'CreateAccount':
        response = createaccount(Accountnumber, Name, Creditamt, Contactnum)
        return response

def createaccount(Accountnumber, Name, Creditamt, Contactnum):
    table_name = 'customerdetails'

    item = {
        'accountnumber': {'S': Accountnumber},  # Adjust if key name is different
        'name': {'S': Name},
        'balance': {'N': str(Creditamt)},
        'ContactNumber': {'S': Contactnum}
    }

    try:
        # Insert the item into the DynamoDB table
        client.put_item(TableName=table_name, Item=item)
        
        # Construct the response message
        message = f'Account has been created successfully. Your account number is {Accountnumber}.'
        
        # Return response to Lex Bot
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
        # Handle any errors that occur during the put operation
        error_message = e.response['Error']['Message']
        return {
            "dialogAction": {
                "type": "Close",
                "fulfillmentState": "Failed",
                "message": {
                    "contentType": "PlainText",
                    "content": f'Failed to create account. Error: {error_message}'
                }
            }
        }
