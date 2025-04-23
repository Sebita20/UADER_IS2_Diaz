import os
from abc import ABC, abstractmethod


class Director:
    """Clase que orquesta la construcción del avión."""

    def set_builder(self, builder):
        """Asigna un constructor específico al director."""
        self._builder = builder

    def get_airplane(self):
        """Construye un avión utilizando el constructor asignado."""
        airplane = Airplane()

        airplane.set_body(self._builder.get_body())

        for _ in range(2):
            airplane.attach_engine(self._builder.get_engine())

        for _ in range(2):
            airplane.attach_wing(self._builder.get_wing())

        airplane.set_landing_gear(self._builder.get_landing_gear())

        return airplane


class Airplane:
    """Clase que representa un avión."""

    def __init__(self):
        self._engines = []
        self._wings = []
        self._body = None
        self._landing_gear = None

    def set_body(self, body):
        self._body = body

    def attach_engine(self, engine):
        self._engines.append(engine)

    def attach_wing(self, wing):
        self._wings.append(wing)

    def set_landing_gear(self, landing_gear):
        self._landing_gear = landing_gear

    def specification(self):
        print("Cuerpo: %s" % self._body.shape)
        print("Número de turbinas: %d" % len(self._engines))
        print("Número de alas: %d" % len(self._wings))
        print("Tipo de tren de aterrizaje: %s" % self._landing_gear.type)


class Builder(ABC):
    """Clase abstracta base para el constructor de aviones."""

    @abstractmethod
    def get_engine(self): pass

    @abstractmethod
    def get_wing(self): pass

    @abstractmethod
    def get_body(self): pass

    @abstractmethod
    def get_landing_gear(self): pass


class AirplaneBuilder(Builder):
    """Constructor específico para construir aviones."""

    def get_engine(self):
        return Engine()

    def get_wing(self):
        return Wing()

    def get_body(self):
        return Body()

    def get_landing_gear(self):
        return LandingGear()


class Engine:
    """Clase que representa un motor de avión."""
    pass


class Wing:
    """Clase que representa un ala de avión."""
    pass


class Body:
    """Clase que representa el cuerpo de un avión."""
    def __init__(self):
        self.shape = "Fuselaje estándar"


class LandingGear:
    """Clase que representa el tren de aterrizaje de un avión."""
    def __init__(self):
        self.type = "Retráctil"


def main():
    """Función principal del programa."""
    airplane_builder = AirplaneBuilder()
    director = Director()
    director.set_builder(airplane_builder)
    airplane = director.get_airplane()
    airplane.specification()


if __name__ == "__main__":
    os.system("cls" if os.name == "nt" else "clear")
    print("Ejemplo de un patrón de tipo builder aplicado a la construcción de un avión\n")
    main()