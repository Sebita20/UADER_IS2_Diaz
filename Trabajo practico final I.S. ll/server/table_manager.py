import os
import threading
import boto3
from boto3.dynamodb.conditions import Attr
import json
from botocore.exceptions import ClientError
from decimal import Decimal

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj) 
        return super().default(obj)

class TableManager:
    _instance = None
    _lock = threading.Lock()

    CORPORATE_DATA = os.environ.get('TPFI_CORP_DATA_TABLE', 'CorporateData')
    CORPORATE_LOG = os.environ.get('TPFI_CORP_LOG_TABLE', 'CorporateLog')

    def __init__(self, region_name=None):
        if TableManager._instance is not None:
            raise RuntimeError('Use TableManager.instance()')

        session = boto3.Session(region_name=region_name)
        self.dynamodb = session.resource('dynamodb')
        self.data_table = self.dynamodb.Table(self.CORPORATE_DATA)
        self.log_table = self.dynamodb.Table(self.CORPORATE_LOG)

    @classmethod
    def instance(cls, region_name=None):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = TableManager(region_name=region_name)
        return cls._instance

    def get(self, key):
        try:
            resp = self.data_table.get_item(Key={'id': key})
            return resp.get('Item')
        except ClientError as e:
            raise

    def set(self, key, value_dict):
        item = dict(value_dict)
        item['id'] = key
        try:
            self.data_table.put_item(Item=item)
            return True
        except ClientError:
            raise

    def list(self, simple_filter=None, limit=100):
        try:
            if simple_filter is None:
                resp = self.data_table.scan(Limit=limit)
                return resp.get('Items', [])
            field, op, value = simple_filter
            if op == 'contains':
                fe = Attr(field).contains(value)
                resp = self.data_table.scan(FilterExpression=fe, Limit=limit)
            elif op == '=':
                fe = Attr(field).eq(value)
                resp = self.data_table.scan(FilterExpression=fe, Limit=limit)
            elif op == '>=':
                fe = Attr(field).gte(value)
                resp = self.data_table.scan(FilterExpression=fe, Limit=limit)
            elif op == '<=':
                fe = Attr(field).lte(value)
                resp = self.data_table.scan(FilterExpression=fe, Limit=limit)
            else:
                resp = self.data_table.scan(Limit=limit)
            return resp.get('Items', [])
        except ClientError:
            raise
