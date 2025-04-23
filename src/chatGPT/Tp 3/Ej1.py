class CalcularFactorial:
    _instance = None  # Variable de clase para almacenar la única instancia

    def __new__(cls):
        """
        Método especial que se llama para crear una nueva instancia de la clase.
        Utilizamos este método para asegurarnos de que solo haya una instancia de la clase.
        """
        if cls._instance is None:  # Verifica si ya hay una instancia creada
            cls._instance = super().__new__(cls)  # Crea una nueva instancia si no existe
            cls._instance.result_cache = {}  # Inicializa el caché de resultados
        return cls._instance

    def factorial(self, n):
        """
        Método para calcular el factorial de un número dado.

        Args:
            n (int): El número entero del cual se calculará el factorial.

        Returns:
            int: El factorial del número dado.
        """
        if n in self.result_cache:
            return self.result_cache[n]  # Devuelve el resultado del caché si está disponible
        if n == 0:
            result = 1
        else:
            result = n * self.factorial(n - 1)  # Llamada recursiva para calcular el factorial
        self.result_cache[n] = result  # Almacena el resultado en el caché
        return result


calcular = CalcularFactorial()
print(calcular.factorial(4))
print(calcular.factorial(6))