from app.application.ports import UnitOfWork
from app.domain.order import Order, OrderItem


class CrearOrdenUseCase:
    def __init__(self, uow: UnitOfWork):
        # Inyección de dependencias mediante la interfaz UnitOfWork
        self.uow = uow

    def ejecutar(self, id_orden: str, cliente: str, items_data: list[dict]) -> Order:
        # El bloque 'with' ejecuta el método __enter__ del UoW
        with self.uow:
            # 1. Instanciación del Dominio
            items = [
                OrderItem(nombre=i["nombre"], precio=i["precio"]) for i in items_data
            ]
            nueva_orden = Order(id=id_orden, cliente=cliente, items=items)

            # 2. Persistencia en memoria transaccional
            self.uow.orders.guardar_orden(nueva_orden)

            # 3. Confirmación de la transacción
            self.uow.commit()

            return nueva_orden
