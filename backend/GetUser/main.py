import boto3
import os
import json
      
dynamodb = boto3.resource('dynamodb')
TABLE_NAME = os.environ['TABLE_NAME']
table = dynamodb.Table(TABLE_NAME)

def handler(event, context):
  # TODO: restrict access origin to site 
  response = {
    "headers": {
      'Access-Control-Allow-Origin': '*'
    }
  }

  try:
    username = event["requestContext"]["authorizer"]["claims"]["cognito:username"]
    table_query_resp = table.get_item(Key={'Id':username})
    user =  table_query_resp["Item"]
    filtered_user = {
      "user": {
        "key": user.get("Key", None),
      }
    }

    response["statusCode"] = 200
    response["body"] = json.dumps(filtered_user)


  except Exception as err:
    print("ERR: ", err)
    response["statusCode"] = 500

  return response