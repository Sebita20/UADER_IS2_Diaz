from abc import ABC, abstractmethod


class Numero(ABC):
    """
    Clase base que define la interfaz para representar un número y su método para imprimir su valor actual.
    """

    @abstractmethod
    def imprimir_valor(self) -> None:
        """
        Método abstracto para imprimir el valor del número.
        """
        pass

class OperacionDecorator(Numero):
    """
    Clase base para los decoradores de operación, que envolverán instancias de la clase Numero.
    """

    def __init__(self, numero: Numero) -> None:
        """
        Inicializa el decorador con una instancia de Numero.

        Args:
            numero (Numero): Instancia de la clase Numero.
        """
        self._numero = numero

    def imprimir_valor(self) -> None:
        """
        Método para imprimir el valor del número.
        """
        self._numero.imprimir_valor()


class SumarDosDecorator(OperacionDecorator):
    """
    Decorador para sumar 2 al número.
    """

    def imprimir_valor(self) -> None:
        """
        Método para imprimir el valor del número sumado con 2.
        """
        super().imprimir_valor()
        print(f" + 2 = {self._numero.valor + 2}")


class MultiplicarPorDosDecorator(OperacionDecorator):
    """
    Decorador para multiplicar el número por 2.
    """

    def imprimir_valor(self) -> None:
        """
        Método para imprimir el valor del número multiplicado por 2.
        """
        super().imprimir_valor()
        print(f" * 2 = {self._numero.valor * 2}")


class DividirPorTresDecorator(OperacionDecorator):
    """
    Decorador para dividir el número por 3.
    """

    def imprimir_valor(self) -> None:
        """
        Método para imprimir el valor del número dividido por 3.
        """
        super().imprimir_valor()
        print(f" / 3 = {self._numero.valor / 3}")


class NumeroSimple(Numero):
    """
    Clase concreta para representar un número.
    """

    def __init__(self) -> None:
        """
        Inicializa un objeto NumeroSimple solicitando al usuario un número positivo diferente de cero.
        """
        self.valor = self._obtener_numero()

    def _obtener_numero(self) -> int:
        """
        Método privado para obtener un número positivo diferente de cero desde la entrada del usuario.

        Returns:
            int: Número positivo diferente de cero.
        """
        while True:
            try:
                valor = int(input("Ingrese un número (debe ser positivo y diferente de cero): "))
                if valor <= 0:
                    print("El número debe ser positivo y diferente de cero. Inténtelo de nuevo.")
                else:
                    return valor
            except ValueError:
                print("Por favor, ingrese un número entero válido.")

    def imprimir_valor(self) -> None:
        """
        Método para imprimir el valor del número.
        """
        print(f"Número: {self.valor}")


if __name__ == "__main__":
    # Crear un número simple
    numero = NumeroSimple()
    numero.imprimir_valor()

    print("\nAplicando operaciones:")

    # Aplicar decoradores a la instancia original
    numero_sumar_dos = SumarDosDecorator(numero)
    numero_sumar_dos.imprimir_valor()

    numero_multiplicar_por_dos = MultiplicarPorDosDecorator(numero)
    numero_multiplicar_por_dos.imprimir_valor()

    numero_dividir_por_tres = DividirPorTresDecorator(numero)
    numero_dividir_por_tres.imprimir_valor()