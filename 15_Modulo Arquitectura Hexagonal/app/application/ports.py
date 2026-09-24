from abc import ABC, abstractmethod

from app.domain.order import Order


# Las interfaces se hacen usando la librería abc (Abstract Base Classes).
# El puerto un contrato estricto (como las interfaces en java)
# En este caso ualquiera que
# quiera ser un repositorio, debe tener una función llamada guardar_orden'
class OrderRepository(ABC):
    @abstractmethod
    def guardar_orden(self, orden: Order) -> None:
        pass
