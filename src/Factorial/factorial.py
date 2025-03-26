#!/usr/bin/python
#*-------------------------------------------------------------------------*
#* factorial.py                                                            *
#* calcula el factorial de un número                                       *
#* Dr.P.E.Colla (c) 2022                                                   *
#* Creative commons                                                        *
#*-------------------------------------------------------------------------*
import sys

def factorial(num): 
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

if len(sys.argv) == 1:
    print("Debe informar un número o un rango en formato inicio-fin (ej. 4-8, -10, 5-).")
    sys.exit()

# Obtener el argumento ingresado
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

# Calcular y mostrar factoriales en el rango
for num in range(inicio, fin + 1):
    print(f"Factorial {num}! es {factorial(num)}")
