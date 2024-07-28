import json
import boto3

client = boto3.client('dynamodb')

def lambda_handler(event, context):
    try:
        intent = event['currentIntent']['name']
        Accountnumber = event['currentIntent']['slots']['AccountNumber']
        amt = float(event['currentIntent']['slots']['Amount'])
        password = event['currentIntent']['slots']['Password']

        # Check if the account exists and the password is correct
        response = client.get_item(
            TableName='customerdetails',
            Key={
                'accountnumber': {'S': Accountnumber}
            }
        )

        if 'Item' not in response:
            return create_response("Failed", "Account number is incorrect. Please try again.")

        item = response['Item']
        if item['password']['S'] != password:
            return create_response("Failed", "Password is incorrect. Please try again.")

        if intent == 'Withdraw':
            return withdraw(Accountnumber, amt)

    except Exception as e:
        return create_response("Failed", f"An error occurred. Details: {str(e)}")

def withdraw(Accountnumber, amt):
    try:
        # Get current balance
        response = client.get_item(
            TableName='customerdetails',
            Key={
                'accountnumber': {'S': Accountnumber}
            }
        )

        item = response['Item']
        current_balance = float(item['balance']['N'])

        if current_balance < amt:
            return create_response("Failed", "Insufficient balance. Please try again.")

        # Update balance and last transaction
        new_balance = current_balance - amt
        client.update_item(
            TableName='customerdetails',
            Key={
                'accountnumber': {'S': Accountnumber}
            },
            UpdateExpression='SET balance = :val1, last_transaction = :val2',
            ExpressionAttributeValues={
                ':val1': {'N': str(new_balance)},
                ':val2': {'S': f'Withdrawal of ${amt}'}
            }
        )

        message = f"Withdrawal successful. Remaining balance is ${new_balance}"
        return create_response("Fulfilled", message)

    except Exception as e:
        return create_response("Failed", f"An error occurred during withdrawal. Details: {str(e)}")

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
