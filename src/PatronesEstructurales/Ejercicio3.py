from abc import ABC, abstractmethod


# Definición de la clase base Componente
class Componente(ABC):
    @abstractmethod
    def mostrar(self):
        """Método abstracto para mostrar información del componente."""
        pass


# Clase Pieza que representa una pieza individual
class Pieza(Componente):
    def __init__(self, nombre):
        """Constructor de la clase Pieza. """
        self.nombre = nombre

    def mostrar(self):
        """Muestra información de la pieza."""
        print(f"Pieza: {self.nombre}")


# Clase Subconjunto que representa un conjunto de piezas o subconjuntos
class Subconjunto(Componente):
    def __init__(self, nombre):
        """Constructor de la clase Subconjunto."""
        self.nombre = nombre
        self.componentes = []

    def agregar(self, componente):
        """Agrega un componente al subconjunto.

        Args:
            componente (Componente): Componente a agregar.
        """
        self.componentes.append(componente)

    def mostrar(self):
        """Muestra información del subconjunto y sus componentes."""
        print(f"Subconjunto: {self.nombre}")
        for componente in self.componentes:
            componente.mostrar()


# Creación del producto principal y sus subconjuntos
producto_principal = Subconjunto("Producto Principal")

# Creación de tres subconjuntos
subconjunto_1 = Subconjunto("Subconjunto 1")
subconjunto_2 = Subconjunto("Subconjunto 2")
subconjunto_3 = Subconjunto("Subconjunto 3")

# Agregar piezas a cada subconjunto
for i in range(4):
    subconjunto_1.agregar(Pieza(f"Pieza {i+1}"))
    subconjunto_2.agregar(Pieza(f"Pieza {i+5}"))
    subconjunto_3.agregar(Pieza(f"Pieza {i+9}"))

# Agregar subconjuntos al producto principal
producto_principal.agregar(subconjunto_1)
producto_principal.agregar(subconjunto_2)
producto_principal.agregar(subconjunto_3)

# Mostrar la estructura completa
print("Estructura del producto principal antes de agregar el subconjunto opcional:")
producto_principal.mostrar()

# Agregar un subconjunto opcional adicional
subconjunto_opcional = Subconjunto("Subconjunto Opcional")
for i in range(4):
    subconjunto_opcional.agregar(Pieza(f"Pieza Opcional {i+1}"))

producto_principal.agregar(subconjunto_opcional)

# Mostrar la estructura actualizada
print("\nEstructura del producto principal después de agregar el subconjunto opcional:")
producto_principal.mostrar()