import boto3

client = boto3.client('dynamodb',aws_access_key_id='xxx', aws_secret_access_key='xxx', region_name='us-east-2')


response = client.put_item(
    TableName='cablegate_document',
    Item={
        'name':{'S': 'test'}  # attention syntaxe articuliere
    }
)


# lien utile
# https://sysadmins.co.za/experimenting-the-client-interface-for-dynamodb-in-boto3-with-gamescores/
# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.put_item

