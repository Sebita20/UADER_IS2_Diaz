import argparse
import socket
import json
import uuid

def send_request(host, port, req):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    s.sendall((json.dumps(req) + '\n').encode('utf-8'))
    data = b''
    while True:
        part = s.recv(4096)
        if not part:
            break
        data += part
        if b'\n' in data:
            break
    s.close()
    try:
        line = data.decode('utf-8').split('\n',1)[0]
        return json.loads(line)
    except:
        return {'status':'error','message':'invalid response'}

def parse_filter(raw):
    if not raw:
        return None
    for op in ['>=','<=','=', 'contains']:
        if op in raw:
            parts = raw.split(op)
            field = parts[0].strip()
            value = parts[1].strip()
            try:
                if '.' in value:
                    value = float(value)
                else:
                    value = int(value)
            except:
                value = value.strip('"').strip("'")
            return {'field': field, 'op': op, 'value': value}
    return None

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', default='127.0.0.1')
    parser.add_argument('--port', default=5000, type=int)
    parser.add_argument('--action', required=True, choices=['get','set','list'])
    parser.add_argument('--key')
    parser.add_argument('--value')
    parser.add_argument('--filter')
    args = parser.parse_args()

    req = {'request_id': str(uuid.uuid4()), 'client_id': 'cli-'+str(uuid.uuid4())[:8], 'action': args.action, 'resource':'CorporateData'}
    if args.key:
        req['key'] = args.key
    if args.value:
        try:
            req['value'] = json.loads(args.value)
        except:
            req['value'] = args.value
    if args.filter:
        req['filter'] = parse_filter(args.filter)

    resp = send_request(args.host, args.port, req)
    print(json.dumps(resp, indent=2, ensure_ascii=False))