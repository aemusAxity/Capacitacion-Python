from dataclasses import dataclass, field

from app.domain.events import Event, OrderCreated

# Entidades (reglas de negocio)


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

    # Lista interna para almacenar los eventos generados por esta Entidad
    events: list[Event] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.items:
            raise ValueError("Una orden debe tener al menos un artículo.")

        # Registramos el evento de dominio dentro de la entidad al inicializarse con éxito
        self.events.append(OrderCreated(order_id=self.id))

    @property
    def total(self) -> float:
        return sum(item.precio for item in self.items)
