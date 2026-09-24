from dataclasses import dataclass

# Evento de dominio notificaciones de que el estado interno cambió
# Contiene solo los datos necesarios para identificar qué ocurrió (id)


@dataclass
class Event:
    pass


@dataclass
class OrderCreated(Event):
    order_id: str
