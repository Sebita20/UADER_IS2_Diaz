import argparse
import socket
import threading
import json
from decimal import Decimal
from table_manager import TableManager, DecimalEncoder
from corporate_log import CorporateLog
from observer_manager import ObserverManager

HOST = '0.0.0.0'
PORT = 5000


class ClientHandler(threading.Thread):
    def __init__(self, conn, addr, table_manager, log_writer, observer_mgr):
        super().__init__(daemon=True)
        self.conn = conn
        self.addr = addr
        self.tm = table_manager
        self.log = log_writer
        self.observer = observer_mgr
        self.running = True
        print(f"[INFO] Nuevo cliente conectado desde {addr}")

    def run(self):
        with self.conn:
            buffer = ''
            while self.running:
                try:
                    data = self.conn.recv(4096)
                    if not data:
                        break
                    buffer += data.decode('utf-8')
                    while '\n' in buffer:
                        line, buffer = buffer.split('\n', 1)
                        if not line.strip():
                            continue
                        try:
                            req = json.loads(line)
                        except Exception:
                            resp = {'status': 'error', 'message': 'invalid json'}
                            self._send(resp)
                            continue
                        try:
                            self._process(req)
                        except Exception as e:
                            print(f"[ERROR] Fallo al procesar request: {e}")
                            resp = {'status': 'error', 'message': str(e)}
                            self._send(resp)
                except Exception as e:
                    print(f"[WARN] Conexión cerrada inesperadamente: {e}")
                    break

    def _send(self, obj):
        try:
            s = json.dumps(obj, cls=DecimalEncoder) + '\n'
            self.conn.sendall(s.encode('utf-8'))
        except Exception as e:
            print(f"[WARN] Error al enviar respuesta: {e}")

    def _process(self, req):
        action = req.get('action')
        request_id = req.get('request_id')
        client_id = req.get('client_id', 'unknown')
        resource = req.get('resource', 'CorporateData')

        print(f"[DEBUG] Acción recibida: {action} (cliente: {client_id})")

        if action == "get":
            key = req.get('key')
            if not key:
                self._send({'request_id': request_id, 'status': 'error', 'message': 'key required'})
                return
            result = self.tm.get(key)
            result_json = json.loads(json.dumps(result, cls=DecimalEncoder))
            self.log.write({'request_id': request_id, 'client_id': client_id, 'action': 'get', 'resource': resource, 'key': key})
            self._send({"request_id": request_id, "status": "ok", "data": result_json})
            return

        if action == 'set':
            key = req.get('key')
            value = req.get('value')
            if not key or value is None:
                self._send({'request_id': request_id, 'status': 'error', 'message': 'key and value required'})
                return
            old = self.tm.get(key)
            self.tm.set(key, value)
            self.log.write({
                'request_id': request_id,
                'client_id': client_id,
                'action': 'set',
                'resource': resource,
                'key': key,
                'diff': {'old': old, 'new': value}
            })
            event = {'event': 'update', 'resource': resource, 'key': key, 'data': value, 'diff': {'old': old, 'new': value}, 'origin_request_id': request_id}
            self.observer.notify(event)
            self._send({'request_id': request_id, 'status': 'ok'})
            return

        if action == 'list':
            print("[SERVER] Acción LIST: mostrando registros del CorporateLog")
            logs = self.log.list_logs(limit=req.get('limit', 100))
            self.log.write({'request_id': request_id, 'client_id': client_id, 'action': 'list', 'resource': 'CorporateLog'})
            self._send({'request_id': request_id, 'status': 'ok', 'data': logs})
            return

        if action == 'subscribe':
            filter_raw = req.get('filter')
            filt = None
            if filter_raw:
                filt = (filter_raw.get('field'), filter_raw.get('op'), filter_raw.get('value'))
            client_id = req.get('client_id', 'observer-' + str(self.addr))
            self.observer.subscribe(client_id, filt, self.conn)
            self.log.write({'request_id': request_id, 'client_id': client_id, 'action': 'subscribe', 'resource': resource})
            self._send({'request_id': request_id, 'status': 'ok', 'subscribed': True})
            return

        self.log.write({'request_id': request_id, 'client_id': client_id, 'action': 'unknown', 'resource': resource})
        self._send({'request_id': request_id, 'status': 'error', 'message': 'unknown action'})


def start_server(host, port):
    tm = TableManager.instance()
    logw = CorporateLog()
    observer = ObserverManager()

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((host, port))
    sock.listen(50)
    print(f"\n[SERVER] ProxyServer escuchando en {host}:{port}")
    print("[SERVER] Esperando conexiones de clientes...\n")
    try:
        while True:
            conn, addr = sock.accept()
            handler = ClientHandler(conn, addr, tm, logw, observer)
            handler.start()
    except KeyboardInterrupt:
        print("\n[SERVER] Detenido manualmente.")
    finally:
        sock.close()
        print("[SERVER] Socket cerrado correctamente.")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', default=HOST)
    parser.add_argument('--port', default=PORT, type=int)
    args = parser.parse_args()
    start_server(args.host, args.port)