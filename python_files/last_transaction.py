import json
import boto3
from botocore.exceptions import ClientError

client = boto3.client('dynamodb')

def lambda_handler(event, context):
    intent = event['currentIntent']['name']
    slots = event['currentIntent']['slots']
    Accountnumber = slots['AccountNumber']
    Password = slots['Password']
    
    # Check if slots are filled
    if not Accountnumber:
        return elicit_slot(event, 'AccountNumber', 'Please provide your account number.')
    if not Password:
        return elicit_slot(event, 'Password', 'Please provide your password for verification.')
    
    # Check if the password is correct for the given account number
    try:
        response = client.get_item(
            TableName='customerdetails',
            Key={
                'accountnumber': {'S': Accountnumber}
            }
        )
        
        if 'Item' not in response:
            return create_response("Failed", "Account number is incorrect. Please try again.")
        
        if response['Item']['password']['S'] == Password:
            if intent == 'LastTransaction':
                return lasttransaction(Accountnumber)
        else:
            return create_response("Failed", "Password is incorrect. Please try again.")
    
    except ClientError as e:
        return create_response("Failed", f"Client error: {e.response['Error']['Message']}")
    except Exception as e:
        return create_response("Failed", f"An error occurred: {str(e)}")

def lasttransaction(Accountnumber):
    try:
        response = client.get_item(
            TableName='customerdetails',
            Key={
                'accountnumber': {'S': Accountnumber}
            }
        )
        
        if 'Item' not in response:
            return create_response("Failed", "Account number is incorrect. Please try again.")
        
        if 'last_transaction' in response['Item']:
            last_transaction = response['Item']['last_transaction']['S']
            message = "Last transaction details: " + last_transaction
        else:
            message = "No transaction details available."
        
        return create_response("Fulfilled", message)
    
    except ClientError as e:
        return create_response("Failed", f"Client error: {e.response['Error']['Message']}")
    except Exception as e:
        return create_response("Failed", f"An error occurred: {str(e)}")

def create_response(fulfillment_state, message):
    return {
        "dialogAction": {
            "type": "Close",
            "fulfillmentState": fulfillment_state,
            "message": {
                "contentType": "PlainText",
                "content": message
            }
        }
    }

def elicit_slot(event, slot_to_elicit, message):
    intent_name = event['currentIntent']['name']
    slots = event['currentIntent']['slots']
    return {
        "dialogAction": {
            "type": "ElicitSlot",
            "intentName": intent_name,
            "slots": slots,
            "slotToElicit": slot_to_elicit,
            "message": {
                "contentType": "PlainText",
                "content": message
            }
        }
    }
