import yaml
import json
import boto3
from botocore.exceptions import ClientError

sts = boto3.client('sts')

def is_self_invocation(detail):
    try:
        identity = sts.get_caller_identity()
        if 'userIdentity' in detail:
            if 'arn' in detail['userIdentity'] and 'Arn' in identity:
                if identity['Arn'] == detail['userIdentity']['arn']:
                    return True
    except ClientError as e:
        print('STS Error: {0}'.format(e))

    return False

def handler(event, context):

    if 'detail' in event:
        detail = event['detail']
        if is_self_invocation(detail):
            return json.dumps({
                'result': 'FAILURE',
                'data': 'Self invocation via CloudWatch Event'
            })
        if 'requestParameters' in detail:
            print(detail)
            # do something with the event
        if 'resources' in detail:
            print(detail['resources'])
            # do something with the event resources

    return return json.dumps({
        'result': 'SUCCESS',
        'data': 'It worked!'
    })
