#iterador
class ReverseIterator:
    def __init__(self, data):
        self.data = data
        self.index = len(data)

    def __iter__(self):
        return self

    def __next__(self):
        if self.index <= 0:
            raise StopIteration
        self.index -= 1
        return self.data[self.index]


class ForwardIterator:
    def __init__(self, data):
        self.data = data
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index >= len(self.data):
            raise StopIteration
        self.index += 1
        return self.data[self.index - 1]


class BidirectionalIterator:
    def __init__(self, data):
        self.forward_iterator = ForwardIterator(data)
        self.reverse_iterator = ReverseIterator(data)

    def forward(self):

        return self.forward_iterator

    def reverse(self):
        return self.reverse_iterator


# Ejemplo de uso:
cadena = "Hola Mundo"

# Iteración en sentido directo
print("Sentido directo:")
for char in BidirectionalIterator(cadena).forward():
    print(char)

# Iteración en sentido inverso
print("\nSentido inverso:")
for char in BidirectionalIterator(cadena).reverse():
    print(char)