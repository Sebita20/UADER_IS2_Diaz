#Observer
class Subject:
    def __init__(self):
        self._observers = []

    def attach(self, observer):
        self._observers.append(observer)

    def detach(self, observer):
        self._observers.remove(observer)

    def notify(self, event):
        for observer in self._observers:
            observer.update(event)


class Observer:
    def update(self, event):
        pass


class SpecificObserver(Observer):
    def __init__(self, observer_id):
        self._observer_id = observer_id

    def update(self, event):
        if event == self._observer_id:
            print(f"Mensaje emitido para el ID {self._observer_id}: {event}")


# Crear el subject
subject = Subject()

# Crear observadores específicos con IDs únicos
observer1 = SpecificObserver("ABCD")
observer2 = SpecificObserver("EFGH")
observer3 = SpecificObserver("IJKL")
observer4 = SpecificObserver("MNOP")

# Suscribir los observadores al subject
subject.attach(observer1)
subject.attach(observer2)
subject.attach(observer3)
subject.attach(observer4)

# Emitir 8 IDs
ids_emitted = ["WXYZ", "ABCD", "EFGH", "IJKL", "MNOP", "QRST", "EFGH", "MNOP"]

# Notificar a los observadores sobre los IDs emitidos
for id_emitted in ids_emitted:
    subject.notify(id_emitted)