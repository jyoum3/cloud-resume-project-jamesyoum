import json
import os
import boto3
from botocore.exceptions import ClientError


dynamodb = boto3.resource('dynamodb', region_name=os.environ.get('AWS_REGION', 'us-east-1'))


TABLE_NAME = os.environ.get('DYNAMODB_TABLE_NAME', 'ResumeVisitorCounter')
ITEM_ID = 'visitor_count' 

def lambda_handler(event, context):
    """
    AWS Lambda handler function for the visitor counter.
    Handles both GET and POST requests.
    """
    print(f"Received event: {json.dumps(event)}")

    http_method = event.get('requestContext', {}).get('http', {}).get('method')
    if not http_method:
        http_method = event.get('httpMethod')

    try:
        table = dynamodb.Table(TABLE_NAME)

        if http_method == 'POST':
            print(f"Attempting to increment item in table: {TABLE_NAME}")
            response = table.update_item(
                Key={'id': ITEM_ID},
                UpdateExpression='SET #count = if_not_exists(#count, :start) + :inc',
                ExpressionAttributeNames={
                    '#count': 'visits'
                },
                ExpressionAttributeValues={
                    ':inc': 1,
                    ':start': 0
                },
                ReturnValues='UPDATED_NEW'
            )
            print(f"DynamoDB update_item response: {response}")

            new_count = int(response['Attributes']['visits'])
            print(f"Successfully incremented count to: {new_count}")
            
            return {
                'statusCode': 200,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': 'https://resumejamesyoum.com', 
                    'Access-Control-Allow-Methods': 'GET,POST,OPTIONS',
                    'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token'
                },
                'body': json.dumps({'count': new_count})
            }

        elif http_method == 'GET':
            print(f"Attempting to get item from table: {TABLE_NAME}")
            response = table.get_item(Key={'id': ITEM_ID})
            item = response.get('Item')
            count = int(item['visits']) if item and 'visits' in item else 0
            print(f"Successfully retrieved count: {count}")

            return {
                'statusCode': 200,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': 'https://resumejamesyoum.com', 
                    'Access-Control-Allow-Methods': 'GET,POST,OPTIONS',
                    'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token'
                },
                'body': json.dumps({'count': count})
            }
        
        else: 
            print(f"Received OPTIONS request.")
            return {
                'statusCode': 200,
                'headers': {
                    'Access-Control-Allow-Origin': 'https://resumejamesyoum.com', 
                    'Access-Control-Allow-Methods': 'GET,POST,OPTIONS',
                    'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token'
                },
                'body': '' 
            }

    except ClientError as e:
        error_message = e.response.get('Error', {}).get('Message', 'Unknown DynamoDB error')
        error_code = e.response.get('Error', {}).get('Code', 'UnknownCode')
        print(f"DynamoDB ClientError: Code={error_code}, Message={error_message}")
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': 'https://resumejamesyoum.com', 
                'Access-Control-Allow-Methods': 'GET,POST,OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token'
            },
            'body': json.dumps({'error': 'Failed to process visitor count', 'details': error_message})
        }
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': 'https://resumejamesyoum.com', 
                'Access-Control-Allow-Methods': 'GET,POST,OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token'
            },
            'body': json.dumps({'error': 'An internal server error occurred', 'details': str(e)})
        }