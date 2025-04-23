from abc import ABC, abstractmethod


# Definimos la clase abstracta HamburguesaFactory que servirá como la base para las fábricas concretas.
class HamburguesaFactory(ABC):
    @abstractmethod
    def crear_hamburguesa(self, nombre):
        pass


# Implementamos una fábrica concreta para cada método de entrega.
class MostradorFactory(HamburguesaFactory):
    def crear_hamburguesa(self, nombre):
        return HamburguesaMostrador(nombre)


class ClienteFactory(HamburguesaFactory):
    def crear_hamburguesa(self, nombre):
        return HamburguesaCliente(nombre)


class DeliveryFactory(HamburguesaFactory):
    def crear_hamburguesa(self, nombre):
        return HamburguesaDelivery(nombre)


# Creamos la clase base Hamburguesa.
class Hamburguesa:
    def __init__(self, nombre):
        self.nombre = nombre

    @abstractmethod
    def entregar(self):
        pass


# Implementamos las subclases de Hamburguesa para cada método de entrega.
class HamburguesaMostrador(Hamburguesa):
    def entregar(self):
        return f"La hamburguesa {self.nombre} está lista para ser recogida en el mostrador."


class HamburguesaCliente(Hamburguesa):
    def entregar(self):
        return f"La hamburguesa {self.nombre} ha sido entregada al cliente."


class HamburguesaDelivery(Hamburguesa):
    def entregar(self):
        return f"La hamburguesa {self.nombre} será enviada por delivery."


# Ejemplo de uso del Factory Method
def main():
    # Seleccionamos una fábrica concreta según el método de entrega deseado.
    factory = DeliveryFactory()

    # Usamos la fábrica para crear una hamburguesa con el nombre "Especial".
    hamburguesa = factory.crear_hamburguesa("Especial")

    # Entregamos la hamburguesa según el método seleccionado.
    print(hamburguesa.entregar())


if __name__ == "__main__":
    main()