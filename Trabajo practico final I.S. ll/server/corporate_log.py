import boto3
import time
import os
from botocore.exceptions import ClientError

class CorporateLog:

    def __init__(self, region_name='us-east-1'):
        self.dynamodb = boto3.resource('dynamodb', region_name=region_name)
        table_name = os.environ.get('TPFI_CORP_LOG_TABLE', 'CorporateLog')
        self.table = self.dynamodb.Table(table_name)
        print(f"[CorporateLog] Conectado a tabla DynamoDB: {table_name}")

    def write(self, entry: dict):
        if not entry:
            return False
        entry = dict(entry)
        entry['timestamp'] = int(time.time())
        try:
            self.table.put_item(Item=entry)
            print(f"[CorporateLog] Log guardado: {entry.get('action')} (key={entry.get('key')})")
            return True
        except ClientError as e:
            print(f"[CorporateLog] Error escribiendo log: {e}")
            return False

    def list_logs(self, limit=100):
        try:
            response = self.table.scan(Limit=limit)
            items = response.get('Items', [])
            # convertir timestamp a int si viene como string
            for i in items:
                if 'timestamp' in i:
                    try:
                        i['timestamp'] = int(i['timestamp'])
                    except Exception:
                        i['timestamp'] = 0
            items.sort(key=lambda x: x.get('timestamp', 0), reverse=True)
            return items
        except ClientError as e:
            print(f"[CorporateLog] Error leyendo logs: {e}")
            return []