from abc import ABC, abstractmethod


class Factura(ABC):
    """
    Interfaz base para las clases de facturas.
    """
    @abstractmethod
    def generar_factura(self):
        """
        Método abstracto para generar la factura.
        """
        pass

class FacturaFactory:
    """
    Fábrica para crear diferentes tipos de facturas.
    """

    @staticmethod
    def crear_factura(importe_total, condicion_impositiva):
        """
        Método estático para crear una factura según la condición impositiva del cliente.

        Args:
        importe_total (float): El importe total de la factura.
        condicion_impositiva (str): La condición impositiva del cliente (IVA Responsable, IVA No Inscripto, IVA Exento).

        Returns:
        Factura: Una instancia de la clase Factura correspondiente.
        """
        if condicion_impositiva == "IVA Responsable":
            return FacturaIVAResponsable(importe_total)
        elif condicion_impositiva == "IVA No Inscripto":
            return FacturaIVANoInscripto(importe_total)
        elif condicion_impositiva == "IVA Exento":
            return FacturaIVAExento(importe_total)
        else:
            raise ValueError("Condición impositiva no válida")


class FacturaIVAResponsable(Factura):
    """
    Clase para generar facturas con IVA Responsable.
    """
    def __init__(self, importe_total):
        self.importe_total = importe_total

    def generar_factura(self):
        impuesto = self.importe_total * 0.21
        total_con_impuesto = self.importe_total + impuesto
        return f"Factura para IVA Responsable - Importe total: ${total_con_impuesto:.2f} (IVA incluido)"


class FacturaIVANoInscripto(Factura):
    """
    Clase para generar facturas con IVA No Inscripto.
    """
    def __init__(self, importe_total):
        self.importe_total = importe_total

    def generar_factura(self):
        return f"Factura para IVA No Inscripto - Importe total: ${self.importe_total:.2f}"


class FacturaIVAExento(Factura):
    """
    Clase para generar facturas con IVA Exento.
    """
    def __init__(self, importe_total):
        self.importe_total = importe_total

    def generar_factura(self):
        return f"Factura para IVA Exento - Importe total: ${self.importe_total:.2f}"


# Ejemplo de uso
factura1 = FacturaFactory.crear_factura(1000, "IVA Responsable")
print(factura1.generar_factura())

factura2 = FacturaFactory.crear_factura(800, "IVA No Inscripto")
print(factura2.generar_factura())

factura3 = FacturaFactory.crear_factura(500, "IVA Exento")
print(factura3.generar_factura())