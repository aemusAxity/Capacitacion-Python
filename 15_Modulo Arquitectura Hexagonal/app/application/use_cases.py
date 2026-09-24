from app.application.ports import OrderRepository
from app.domain.order import Order, OrderItem

# Los casos de uso los cuales reciben los datos,
# construyen las clases del Dominio (donde viven las reglas de negocio) y
# decirle a la BD que guarde la información


# CASO DE USO (Servicio de Aplicación)
# Orquesta el flujo de creación de una orden. No contiene reglas de negocio puras
class CrearOrdenUseCase:
    def __init__(self, repositorio: OrderRepository):
        # Recibimos la interfaz (puerto)
        self.repositorio = repositorio

    def ejecutar(self, id_orden: str, cliente: str, items_data: list[dict]) -> Order:
        # 1. Convertir los datos crudos a Entidades de Dominio.
        items = [OrderItem(nombre=i["nombre"], precio=i["precio"]) for i in items_data]
        nueva_orden = Order(id=id_orden, cliente=cliente, items=items)

        # 2. Usar el puerto (interfaz) para guardar la orden (sin saber qué base de datos es)
        self.repositorio.guardar_orden(nueva_orden)

        return nueva_orden
