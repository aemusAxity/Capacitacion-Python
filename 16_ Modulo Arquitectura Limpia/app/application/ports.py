from abc import ABC, abstractmethod
from typing import Self

from app.domain.order import Order


class OrderRepository(ABC):
    @abstractmethod
    def guardar_orden(self, orden: Order) -> None:
        pass


# La interfaz del UoW exige proveer acceso al repositorio
class UnitOfWork(ABC):

    orders: OrderRepository

    @abstractmethod
    def __enter__(self) -> Self:
        pass

    @abstractmethod
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        pass

    @abstractmethod
    def commit(self) -> None:
        pass

    @abstractmethod
    def rollback(self) -> None:
        pass
