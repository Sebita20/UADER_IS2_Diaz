import boto3
import os

REGION = os.environ.get('AWS_REGION') or os.environ.get('AWS_DEFAULT_REGION') or 'us-east-1'
DATA_TABLE = os.environ.get('TPFI_CORP_DATA_TABLE','CorporateData')
LOG_TABLE = os.environ.get('TPFI_CORP_LOG_TABLE','CorporateLog')

def create_table(dynamodb, name, key_schema, attr_defs, billing_mode='PAY_PER_REQUEST'):
    existing = [t.name for t in dynamodb.tables.all()]
    if name in existing:
        print(f"Table {name} already exists.")
        return dynamodb.Table(name)
    print(f"Creating table {name} ...")
    table = dynamodb.create_table(
        TableName=name,
        KeySchema=key_schema,
        AttributeDefinitions=attr_defs,
        BillingMode=billing_mode
    )
    print("Waiting for table to be ACTIVE...")
    table.wait_until_exists()
    print("Created.")
    return table

def main():
    session = boto3.Session(region_name=REGION)
    dynamodb = session.resource('dynamodb')
    create_table(dynamodb, DATA_TABLE,
                 key_schema=[{'AttributeName':'id','KeyType':'HASH'}],
                 attr_defs=[{'AttributeName':'id','AttributeType':'S'}])
    create_table(dynamodb, LOG_TABLE,
                 key_schema=[{'AttributeName':'id','KeyType':'HASH'}],
                 attr_defs=[{'AttributeName':'id','AttributeType':'S'}])
    print("Done.")

if __name__ == '_main_':
    main()