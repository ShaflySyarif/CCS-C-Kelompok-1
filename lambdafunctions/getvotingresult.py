import json
import boto3

dynamodb = boto3.client('dynamodb')

def lambda_handler(event, context):
    try:
        # 1. EXTRACT THE USER'S EMAIL FROM THE VIP PASS
        claims = event.get('requestContext', {}).get('authorizer', {}).get('jwt', {}).get('claims', {})
        user_email = claims.get('email', '')
        
        # 2. THE ADMIN LIST (Put your exact Cognito test email here)
        ADMIN_EMAILS = ["immpwss@gmail.com"] 
        
        # 3. CHECK THE BOUNCER'S LIST
        if user_email not in ADMIN_EMAILS:
            return {
                'statusCode': 200, # Returning 200 so our frontend catches the JSON error nicely
                'headers': {'Access-Control-Allow-Origin': '*'},
                'body': json.dumps({'error': f'Access Denied: {user_email} is not an admin.'})
            }

        # 4. IF THEY ARE AN ADMIN, FETCH THE RESULTS
        response = dynamodb.scan(TableName='ElectionResults')
        items = response.get('Items', [])
        
        results = {}
        for item in items:
            candidate = item['candidate_id']['S']
            votes = int(item['vote_count']['N'])
            results[candidate] = votes
            
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type,Authorization',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
            },
            'body': json.dumps({'results': results})
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'error': 'Could not fetch results.'})
        }