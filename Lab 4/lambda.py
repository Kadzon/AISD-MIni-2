import json
import logging
import boto3

# Get the service resource.

client = boto3.client('dynamodb')
    
def lambda_handler(event, context):
    # TODO implement

    print(event)
    for rec in event['Records']:
        print(rec)
        if rec['eventName'] == 'INSERT':
            UpdateItem = rec['dynamodb']['NewImage']
            print(UpdateItem)

            pred = UpdateItem["Class"]["S"]
            actual = UpdateItem["Actual"]["S"]
            prob = UpdateItem["Probability"]["S"]

            if(pred != actual) or (float(prob) < 0.9):
                # lab4 code goes here
                response = client.put_item(TableName='IrisExtendedRetrain', Item=UpdateItem)
                print(response)

    return {
        'statusCode': 200,
        'body': json.dumps('IrisExtendedRetrain Lambda return')
        }