"""
Este programa permite recuperar una clave desde un archivo JSON.
Uso:
    python getJason.py <archivo_json> [clave]

- <archivo_json>: ruta al archivo JSON (obligatorio)
- [clave]: clave a recuperar del JSON (opcional, por defecto 'token1')
"""

import json
import sys


def load_json(filename):
    # Carga el contenido de un archivo JSON.
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: El archivo '{filename}' no existe.", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: El archivo '{filename}' no contiene JSON válido.\n{e}", file=sys.stderr)
        sys.exit(1)


def get_json_key(json_data, key):
    # Devuelve el valor de una clave en el diccionario JSON.
    try:
        return json_data[key]
    except KeyError:
        print(f"Error: La clave '{key}' no se encontró en el archivo JSON.", file=sys.stderr)
        sys.exit(1)


def main():
    if len(sys.argv) < 2:
        print("Uso: python getJason.py <archivo_json> [clave]", file=sys.stderr)
        sys.exit(1)

    json_file = sys.argv[1]
    json_key = sys.argv[2] if len(sys.argv) > 2 else "token1"

    json_data = load_json(json_file)
    value = get_json_key(json_data, json_key)

    print(value)


if __name__ == "__main__":
    main()