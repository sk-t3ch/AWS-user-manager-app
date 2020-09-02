import boto3
from boto3.dynamodb.conditions import Key
import os
import json

dynamodb = boto3.resource('dynamodb')
TABLE_NAME = os.environ['TABLE_NAME']
table = dynamodb.Table(TABLE_NAME)


def handler(event, context):
    """
    Test Key - this functions expects an API key.
    The API key is searched for on the user table secondary index and credit decremented.
    """
    # TODO: restrict access origin to site 
    response = {
        'isBase64Encoded': False,
        'headers': {
            'access-control-allow-methods': 'POST',
            'Access-Control-Allow-Origin': '*',
            'access-control-allow-headers': 'Content-Type, Access-Control-Allow-Headers'
        },
        'statusCode': 200
    }
    if event['httpMethod'] == 'OPTIONS':
        return response
    try:
        count = "UNKNOWN"
        key = json.loads(event["body"]).get("key")
        table_query_resp = table.query(
            IndexName='KeyLookup',
            KeyConditionExpression=Key('Key').eq(key)
        )
        item = table_query_resp["Items"][0]
        count = item["Count"]
        id = item["Id"]
        
        table_update_resp = table.update_item(
            Key={
                'Id': id,
            },
            UpdateExpression="set #c = #c +:num",
            ExpressionAttributeNames={
                "#c": "Count"
            },
            ExpressionAttributeValues={
                ':num': 1,
            },
            ReturnValues="UPDATED_NEW"
        )

        count = table_update_resp["Attributes"]["Count"]
        response["body"] = json.dumps({"COUNT": int(count)})
        response["statusCode"] = 200

    except Exception as err:
        print("ERR: ", err)
        response["statusCode"] = 500

    return response

