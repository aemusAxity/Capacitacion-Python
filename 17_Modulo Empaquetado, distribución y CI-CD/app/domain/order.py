from dataclasses import dataclass

# Es el Dominio
# Regla de negocio 1: Una orden debe calcular su total automáticamente
# Regla de negocio 2: No se puede crear una orden sin ítems


@dataclass
class OrderItem:
    nombre: str
    precio: float


@dataclass
class Order:
    id: str
    cliente: str
    items: list[OrderItem]
    status: str = "PENDIENTE"

    # Esta función se ejecuta sola al crear la clase para validar las reglas de negocio
    def __post_init__(self) -> None:
        if not self.items:
            raise ValueError("Una orden debe tener al menos un artículo.")

    @property
    def total(self) -> float:
        return sum(item.precio for item in self.items)

    def marcar_como_pagada(self) -> None:
        self.status = "PAGADA"
