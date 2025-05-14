#Cadena de responsabilidades
class Handler:
    def __init__(self, successor=None):
        self.successor = successor

    def handle_request(self, number):
        if not self.can_handle(number):
            if self.successor:
                self.successor.handle_request(number)
            else:
                print(f"El número {number} no fue consumido.")

    def can_handle(self, number):
        raise NotImplementedError("Debe implementar este método en las subclases.")

class PrimeHandler(Handler):
    def can_handle(self, number):
        return self.is_prime(number)

    def is_prime(self, number):
        if number < 2:
            return False
        for i in range(2, int(number ** 0.5) + 1):
            if number % i == 0:
                return False
        return True

    def handle_request(self, number):
        if self.can_handle(number):
            print(f"El número {number} es primo.")
        else:
            super().handle_request(number)

class EvenHandler(Handler):
    def can_handle(self, number):
        return number % 2 == 0

    def handle_request(self, number):
        if self.can_handle(number):
            print(f"El número {number} es par.")
        else:
            super().handle_request(number)

class NumberProcessor:
    def __init__(self):
        self.handler_chain = PrimeHandler(EvenHandler())

    def process_numbers(self):
        for number in range(1, 101):
            self.handler_chain.handle_request(number)


if __name__ == "__main__":
    processor = NumberProcessor()
    processor.process_numbers()