import json
import boto3
import traceback
from botocore.exceptions import ClientError

dynamodb = boto3.client('dynamodb')

def lambda_handler(event, context):
    print("--- INCOMING EVENT DATA ---")
    print(json.dumps(event)) # This lets us see exactly what API Gateway sent!
    
    try:
        body = json.loads(event.get('body', '{}'))
        candidate_selection = body.get('candidate_id')
        
        # COGNITO USER (The VIP Door)
        if 'authorizer' in event.get('requestContext', {}):
            print("Detected Authorizer block. Extracting user...")
            # HTTP APIs usually hide the claims here
            user_id = event['requestContext']['authorizer']['jwt']['claims']['sub']
            print(f"User ID extracted: {user_id}")
            
            response = dynamodb.transact_write_items(
                TransactItems=[
                    {
                        'Put': {
                            'TableName': 'VoterHistory',
                            'Item': {'user_id': {'S': user_id}},
                            'ConditionExpression': 'attribute_not_exists(user_id)' 
                        }
                    },
                    {
                        'Update': {
                            'TableName': 'ElectionResults',
                            'Key': {'candidate_id': {'S': candidate_selection}},
                            'UpdateExpression': 'ADD vote_count :inc',
                            'ExpressionAttributeValues': {':inc': {'N': '1'}}
                        }
                    }
                ]
            )
            message = 'Vote cast successfully via User Account!'

        # ONE-TIME TOKEN (The Open Door)
        else:
            print("No Authorizer found. Processing as Token...")
            user_token = body.get('token_id')
            if not user_token:
                raise ValueError("Missing token_id")

            response = dynamodb.transact_write_items(
                TransactItems=[
                    {
                        'Update': {
                            'TableName': 'VoterTokens',
                            'Key': {'token_id': {'S': user_token}},
                            'UpdateExpression': 'SET is_used = :true_val',
                            'ConditionExpression': 'is_used = :false_val',
                            'ExpressionAttributeValues': {
                                ':true_val': {'BOOL': True},
                                ':false_val': {'BOOL': False}
                            }
                        }
                    },
                    {
                        'Update': {
                            'TableName': 'ElectionResults',
                            'Key': {'candidate_id': {'S': candidate_selection}},
                            'UpdateExpression': 'ADD vote_count :inc',
                            'ExpressionAttributeValues': {':inc': {'N': '1'}}
                        }
                    }
                ]
            )
            message = 'Vote cast successfully via Token!'

        return {
            'statusCode': 200,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'message': message})
        }
        
    except ClientError as e:
        print("--- DYNAMODB ERROR ---")
        print(e)
        return {
            'statusCode': 200, 
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'error': 'Vote failed: Token used or User already voted.'})
        }
            
    except Exception as e:
        print("--- PYTHON CRASHED ---")
        traceback.print_exc() # This prints the exact line number of the crash
        return {
            'statusCode': 200,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'error': f'Code Error: {str(e)}'})
        }