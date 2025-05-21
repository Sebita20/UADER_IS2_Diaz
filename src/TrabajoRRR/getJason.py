# Este programa recupera una clave (por defecto "token1") desde el archivo "sitedata.json"

import os
import json
import sys

script_dir = os.path.dirname(os.path.abspath(__file__))
jsonfile = os.path.join(script_dir, 'sitedata.json')
jsonkey = sys.argv[1] if len(sys.argv) > 1 else 'token1'

try:
    with open(jsonfile, 'r') as myfile:
        data = myfile.read()

    obj = json.loads(data)

    if jsonkey in obj:
        print(str(obj[jsonkey]))
    else:
        print(f"Error: La clave '{jsonkey}' no se encuentra en '{jsonfile}'.")

except FileNotFoundError:
    print(f"Error: El archivo '{jsonfile}' no existe.")
except json.JSONDecodeError:
    print(f"Error: El archivo '{jsonfile}' no contiene un JSON válido.")
except Exception as e:
    print(f"Error inesperado: {e}")