import os


class Ping:
    def __init__(self):
        pass

    def execute(self, ip_address):
        if not ip_address.startswith("192."):
            print("La dirección IP debe comenzar con '192.'")
            return

        print(f"Pinging {ip_address}...")
        for _ in range(10):
            response = os.system(f"ping -c 1 {ip_address}")
            if response == 0:
                print(f"Respuesta de {ip_address}: host activo")
            else:
                print(f"No se pudo alcanzar {ip_address}")

    def executefree(self, ip_address):
        print(f"Pinging {ip_address}...")
        for _ in range(10):
            response = os.system(f"ping -c 1 {ip_address}")
            if response == 0:
                print(f"Respuesta de {ip_address}: host activo")
            else:
                print(f"No se pudo alcanzar {ip_address}")


class PingProxy:
    def __init__(self):
        self.ping = Ping()

    def execute(self, ip_address):
        if ip_address == "192.168.0.254":
            self.ping.executefree("www.google.com")
        else:
            self.ping.execute(ip_address)

# Ej de su uso:

ping_proxy = PingProxy()
ping_proxy.execute("192.168.0.1")  # Realizará ping a la dirección IP
ping_proxy.execute("192.168.0.254")  # Realizará ping a www.google.com usando executefree
ping_proxy.execute("10.0.0.1")  # Intentará realizar ping a la dirección IP, pero no comenzando con "192."