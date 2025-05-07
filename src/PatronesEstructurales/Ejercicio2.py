class LaminaAcero:
    """
    Clase lámina de acero.
    """
    def __init__(self, espesor, ancho, tren_laminador):
        """
        Constructor
        """
        self.espesor = espesor
        self.ancho = ancho
        self.tren_laminador = tren_laminador

    def producir(self):
        """
        Método que inicia el proceso de producción de la lámina de acero utilizando el tren laminador especificado.
        """
        self.tren_laminador.producir_lamina(self)


class TrenLaminador:
    """
    Clase base que representa un tren laminador genérico.
    """
    def producir_lamina(self, lamina):
        """
        Método abstracto para producir una lámina de acero.

        Args:
            lamina (LaminaAcero): La lámina de acero que se va a producir.
        """
        pass


class TrenLaminador5Metros(TrenLaminador):
    """
    Clase que representa un tren laminador de 5 metros de longitud.
    """
    def producir_lamina(self, lamina):
        """
        Método para producir una lámina de acero en un tren laminador de 5 metros.

        Args:
            lamina (LaminaAcero): La lámina de acero que se va a producir.
        """
        print(f"Produciendo lámina de {lamina.espesor}\" de espesor y {lamina.ancho} metros de ancho en el tren laminador de 5 metros.")


class TrenLaminador10Metros(TrenLaminador):
    """
    Clase que representa un tren laminador de 10 metros de longitud.
    """
    def producir_lamina(self, lamina):
        """
        Método para producir una lámina de acero en un tren laminador de 10 metros.

        Args:
            lamina (LaminaAcero): La lámina de acero que se va a producir.
        """
        print(f"Produciendo lámina de {lamina.espesor}\" de espesor y {lamina.ancho} metros de ancho en el tren laminador de 10 metros.")

# Ejemplo de uso


if __name__ == "__main__":
    # Creamos una lámina de acero de 1.5 metros de ancho y la enviamos a producir en un tren laminador de 5 metros
    lamina = LaminaAcero(0.5, 1.5, TrenLaminador5Metros())
    lamina.producir()

    # Creamos otra lámina de acero de 1.5 metros de ancho y la enviamos a producir en un tren laminador de 10 metros
    otra_lamina = LaminaAcero(0.5, 1.5, TrenLaminador10Metros())
    otra_lamina.producir()