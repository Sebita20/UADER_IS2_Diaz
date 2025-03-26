#!/usr/bin/python
#*-------------------------------------------------------------------------*
#* factorial.py                                                            *
#* calcula el factorial de un número                                       *
#* Dr.P.E.Colla (c) 2022                                                   *
#* Creative commons                                                        *
#*-------------------------------------------------------------------------*
import sys

class Factorial:
    def __init__(self):
        pass

    def calcular(self, num):
        """Calcula el factorial de un número dado."""
        if num < 0:
            print(f"Factorial de un número negativo ({num}) no existe")
            return 0
        elif num == 0:
            return 1
        else:
            fact = 1
            while num > 1:
                fact *= num
                num -= 1
            return fact

    def run(self, min_val, max_val):
        """Calcula el factorial de todos los números en el rango [min_val, max_val]."""
        for num in range(min_val, max_val + 1):
            print(f"Factorial {num}! es {self.calcular(num)}")


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("Debe informar un número o un rango en formato inicio-fin (ej. 4-8, -10, 5-).")
        sys.exit()

    entrada = sys.argv[1]

    try:
        if '-' in entrada:
            if entrada.startswith('-'):  # Caso "-10" → de 1 a 10
                inicio, fin = 1, int(entrada[1:])
            elif entrada.endswith('-'):  # Caso "5-" → de 5 a 60
                inicio, fin = int(entrada[:-1]), 60
            else:  # Caso "4-8" → de 4 a 8
                inicio, fin = map(int, entrada.split('-'))

            if inicio > fin:
                print("El primer número debe ser menor o igual al segundo en el rango.")
                sys.exit()
        else:  # Caso único número "5"
            inicio = fin = int(entrada)

    except ValueError:
        print("Formato incorrecto. Use números enteros en formato inicio-fin (ej. 4-8, -10, 5-).")
        sys.exit()

    # Crear instancia de Factorial y ejecutar el cálculo
    fact_calc = Factorial()
    fact_calc.run(inicio, fin)