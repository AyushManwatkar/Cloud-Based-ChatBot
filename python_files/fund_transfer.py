import json
import boto3
from botocore.exceptions import ClientError

client = boto3.client('dynamodb')

def lambda_handler(event, context):
    intent = event['currentIntent']['name']
    slots = event['currentIntent']['slots']
    Accountnumber1 = slots.get('Senderacc')
    Accountnumber2 = slots.get('Receiveracc')
    amt = slots.get('Amount')
    password = slots.get('Password')
    
    # Elicit slots in the desired order
    if not Accountnumber1:
        return elicit_slot(event, 'Senderacc', "What is the sender account number?")
    if not Accountnumber2:
        return elicit_slot(event, 'Receiveracc', "What is the receiver account number?")
    if not amt:
        return elicit_slot(event, 'Amount', "What is the amount to transfer?")
    if not password:
        return elicit_slot(event, 'Password', "What is the password?")
    
    try:
        amt = float(amt)
    except ValueError:
        return create_response("Failed", "Invalid amount. Please provide a valid number.")
    
    # Check if the password is correct for the sender account
    try:
        response = client.get_item(
            TableName='customerdetails',
            Key={
                'accountnumber': {'S': Accountnumber1}
            }
        )
        
        if 'Item' in response:
            if response['Item']['password']['S'] == password:
                if intent == 'FundTransfer':
                    return fundtransfer(Accountnumber1, Accountnumber2, amt)
            else:
                return create_response("Failed", "Password is incorrect. Please try again.")
        else:
            return create_response("Failed", "Account number is incorrect. Please try again.")
    
    except ClientError as e:
        return create_response("Failed", f"Client error: {e.response['Error']['Message']}")
    except Exception as e:
        return create_response("Failed", f"An error occurred: {str(e)}")

def fundtransfer(Accountnumber1, Accountnumber2, amt):
    try:
        response1 = client.get_item(
            TableName='customerdetails',
            Key={
                'accountnumber': {'S': Accountnumber1}
            }
        )
        
        response2 = client.get_item(
            TableName='customerdetails',
            Key={
                'accountnumber': {'S': Accountnumber2}
            }
        )
        
        if 'Item' not in response1:
            return create_response("Failed", "Sender account number is incorrect. Please try again.")
        
        if 'Item' not in response2:
            return create_response("Failed", "Receiver account number is incorrect. Please try again.")
        
        if float(response1['Item']['balance']['N']) >= amt:
            newbalance1 = float(response1['Item']['balance']['N']) - amt
            newbalance2 = float(response2['Item']['balance']['N']) + amt
            
            client.update_item(
                TableName='customerdetails',
                Key={
                    'accountnumber': {'S': Accountnumber1}
                },
                UpdateExpression='SET balance = :val1, last_transaction = :val2',
                ExpressionAttributeValues={
                    ':val1': {'N': str(newbalance1)},
                    ':val2': {'S': f'Transferred {amt} to {Accountnumber2}'}
                }
            )
            
            client.update_item(
                TableName='customerdetails',
                Key={
                    'accountnumber': {'S': Accountnumber2}
                },
                UpdateExpression='SET balance = :val1, last_transaction = :val2',
                ExpressionAttributeValues={
                    ':val1': {'N': str(newbalance2)},
                    ':val2': {'S': f'Received {amt} from {Accountnumber1}'}
                }
            )
            
            return create_response("Fulfilled", f"Amount {amt} has been transferred from {Accountnumber1} to {Accountnumber2}")
        else:
            return create_response("Failed", f"Insufficient balance in account {Accountnumber1}.")
    
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
    return {
        "dialogAction": {
            "type": "ElicitSlot",
            "intentName": event['currentIntent']['name'],
            "slots": event['currentIntent']['slots'],
            "slotToElicit": slot_to_elicit,
            "message": {
                "contentType": "PlainText",
                "content": message
            }
        }
    }
