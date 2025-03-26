import matplotlib.pyplot as plt

def collatz_steps(n):
    """Calcula la cantidad de iteraciones para que n llegue a 1 siguiendo la conjetura de Collatz."""
    steps = 0
    while n != 1:
        if n % 2 == 0:
            n = n // 2
        else:
            n = 3 * n + 1
        steps += 1
    return steps

# Calcular el número de iteraciones para cada número de 1 a 10,000
x_values = list(range(1, 10001))
y_values = [collatz_steps(n) for n in x_values]

# Graficar los resultados
plt.figure(figsize=(10, 6))
plt.scatter(y_values, x_values, s=1, color='blue')
plt.xlabel("Número de Iteraciones")
plt.ylabel("Número Inicial (n)")
plt.title("Número de iteraciones para la conjetura de Collatz (1-10,000)")
plt.grid(True)
plt.show()