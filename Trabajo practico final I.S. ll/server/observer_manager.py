import threading
import json

class ObserverManager:
    def __init__(self):
        self._subs = []
        self._lock = threading.Lock()

    def subscribe(self, client_id, filter_tuple, conn):
        with self._lock:
            self._subs.append({'client_id': client_id, 'filter': filter_tuple, 'conn': conn})

    def unsubscribe(self, client_id, conn=None):
        with self._lock:
            self._subs = [s for s in self._subs if not (s['client_id']==client_id and (conn is None or s['conn']==conn))]

    def notify(self, event: dict):
        to_notify = []
        with self._lock:
            for s in self._subs:
                f = s['filter']
                if f is None:
                    to_notify.append(s)
                else:
                    field, op, value = f
                    try:
                        parts = field.split('.')
                        val = event['data']
                        for p in parts:
                            val = val.get(p) if isinstance(val, dict) else None
                        if op == 'contains' and isinstance(val,str) and str(value) in val:
                            to_notify.append(s)
                        elif op == '>=' and isinstance(val,(int,float)) and float(val) >= float(value):
                            to_notify.append(s)
                        elif op == '<=' and isinstance(val,(int,float)) and float(val) <= float(value):
                            to_notify.append(s)
                        elif op == '=' and val == value:
                            to_notify.append(s)
                    except Exception:
                        continue

        for s in to_notify:
            conn = s['conn']
            try:
                msg = json.dumps(event) + "\\n"
                conn.sendall(msg.encode('utf-8'))
            except Exception:
                try:
                    self.unsubscribe(s['client_id'], conn)
                except Exception:
                    pass