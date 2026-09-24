from typing import Self

from app.application.ports import OrderRepository, UnitOfWork
from app.domain.order import Order


# Implementación concreta del Repositorio
class MemoriaOrderRepository(OrderRepository):
    def __init__(self, data_store: dict[str, Order]):
        self.data_store = data_store

    def guardar_orden(self, orden: Order) -> None:
        self.data_store[orden.id] = orden
        print(f"[SQL Simulada] Orden {orden.id} guardada.")


# Implementación del Unit Of Work (Capa 4: Infraestructura)
# Administra la sesión de la base de datos y la transacción.
class MemoriaUnitOfWork(UnitOfWork):
    def __init__(self) -> None:
        # Estado global simulado
        self.session_data: dict[str, Order] = {}
        self.orders = MemoriaOrderRepository(self.session_data)
        self.commited = False

    def __enter__(self) -> Self:
        self.commited = False
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if exc_type is not None:
            self.rollback()

    def commit(self) -> None:
        self.commited = True
        print("[UoW] Transacción confirmada (Commit).")

    def rollback(self) -> None:
        # En memoria, simular un rollback requiere limpiar el diccionario
        self.session_data.clear()
        print("[UoW] Transacción cancelada (Rollback).")
