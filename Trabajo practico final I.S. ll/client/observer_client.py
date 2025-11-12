import argparse
import socket
import json
import uuid

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
    parser.add_argument('--filter')
    parser.add_argument('--out', help='file to append notifications (optional)')
    args = parser.parse_args()

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((args.host, args.port))
    req = {'request_id': str(uuid.uuid4()), 'client_id': 'observer-'+str(uuid.uuid4())[:8],
           'action':'subscribe', 'resource':'CorporateData'}
    if args.filter:
        req['filter'] = parse_filter(args.filter)
    s.sendall((json.dumps(req) + '\n').encode('utf-8'))
    data = b''
    while True:
        part = s.recv(4096)
        if not part:
            break
        data += part
        if b'\n' in data:
            break
    try:
        line = data.decode('utf-8').split('\n',1)[0]
        resp = json.loads(line)
        print('subscribe response:', resp)
    except Exception as e:
        print('subscribe error', e)
        s.close()
        raise SystemExit(1)

    print('Listening for notifications... (Ctrl-C to exit)')
    try:
        buffer = ''
        while True:
            chunk = s.recv(4096)
            if not chunk:
                print('connection closed by server')
                break
            buffer += chunk.decode('utf-8')
            while '\n' in buffer:
                line, buffer = buffer.split('\n',1)
                if not line.strip():
                    continue
                try:
                    evt = json.loads(line)
                    text = json.dumps(evt, ensure_ascii=False)
                    print('EVENT:', text)
                    if args.out:
                        with open(args.out,'a',encoding='utf-8') as f:
                            f.write(text + '\\n')
                except Exception as e:
                    print('bad event', e)
    except KeyboardInterrupt:
        print('exiting')
    finally:
        s.close()