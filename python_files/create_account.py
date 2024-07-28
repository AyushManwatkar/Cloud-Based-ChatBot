import json
import boto3
import random
import string

client = boto3.client('dynamodb')

def lambda_handler(event, context):
    intent = event['currentIntent']['name']
    slots = event['currentIntent']['slots']

    if intent == 'CreateAccount':
        Name = slots['Name']
        Creditamt = slots['CreditAmount']
        Contactnum = slots['ContactNumber']
        Password = generate_random_string()
        Accountnumber = generate_ten_digit_number()
        return createaccount(Accountnumber, Name, Creditamt, Contactnum, Password)

def generate_random_string(length=6):
    characters = string.ascii_lowercase + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def generate_ten_digit_number():
    return str(random.randint(1000000000, 9999999999))

def createaccount(Accountnumber, Name, Creditamt, Contactnum, Password):
    item = {
        'accountnumber': {'S': Accountnumber},
        'name': {'S': Name},
        'balance': {'N': str(Creditamt)},
        'ContactNumber': {'S': Contactnum},
        'password': {'S': Password},
        'last_transaction': {'S': 'No transactions yet'}  # Initialize last_transaction
    }
    
    try:
        client.put_item(TableName='customerdetails', Item=item)
        message = f'Account has been created successfully. Your account number is {Accountnumber} and password is {Password}.'
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
        message = f'Failed to create account. Error: {str(e)}'
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
