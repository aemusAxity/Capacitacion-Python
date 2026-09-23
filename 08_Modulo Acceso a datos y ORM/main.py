import logging
from pathlib import Path

# Importamos el modelo del archivo models.py
from models import Order, OrderItem, User
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

# 0. Configuracion logger
carpeta_logs = Path("logs")
carpeta_logs.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(carpeta_logs / "db_ordenes.log", encoding="utf-8"),
        logging.StreamHandler(),
    ],
)
log = logging.getLogger(__name__)


# 1. Config. de la BD
engine = create_engine("sqlite:///bd_ordenes.db", echo=False)

# 2. CRUD


def ejecutar_crud_demo():

    # Conexion con la DB
    with Session(engine) as session:

        log.info("--- CREATE: Agregando usuarios y su orden ---")

        usuario1 = User(nombre="Pedro Hernandez", email="pedro@ejemplo.com")
        usuario2 = User(nombre="Alicia Espinoza", email="alicia@ejemplo.com")

        # Creamos una orden y se le asigna al usuario
        orden_1 = Order(estado="PENDIENTE")
        orden_2 = Order(estado="PAGADO")

        orden_1.items.append(
            OrderItem(producto="Laptop Gamer", cantidad=1, precio_unitario=1500.00)
        )
        orden_1.items.append(
            OrderItem(producto="Mouse", cantidad=2, precio_unitario=25.50)
        )

        orden_2.items.append(
            OrderItem(producto="USB", cantidad=1, precio_unitario=50.00)
        )

        # Conectamos la orden al usuario
        usuario1.orders.append(orden_1)
        usuario2.orders.append(orden_2)

        # Guardamos en la BD
        session.add(usuario1)
        session.add(usuario2)
        session.commit()  # El commit hace el guardado final (Transacción)
        log.info(f"Usuario guardado con ID: {usuario1.id}")
        log.info(f"Usuario guardado con ID: {usuario2.id}")

        log.info("\n--- READ: Buscando un usuario en la BD ---")

        # SQLAlchemy 2.0 usa 'select' para construir las consultas
        consulta = select(User).where(User.email == "pedro@ejemplo.com")

        # Ejecutamos la consulta y sacamos el primer resultado
        usuario_db = session.execute(consulta).scalar_one()

        log.info(f"Encontrado: {usuario_db}")
        for orden in usuario_db.orders:
            log.info(f"  -> Tiene la orden: {orden}")
            for item in orden.items:
                log.info(f"      -> Producto: {item.producto} (x{item.cantidad})")

        log.info("\n--- UPDATE: Cambiando el estado de la orden ---")

        orden_a_modificar = usuario_db.orders[0]
        orden_a_modificar.estado = "PAGADO"

        # Hacemos commit para guardar el cambio
        session.commit()
        log.info(
            f"Estado actualizado de la orden ID {orden_a_modificar.id} a: {orden_a_modificar.estado}"
        )

        log.info(
            f"\n--- DELETE: Borrando al usuario {usuario1.id} (y sus órdenes en cascada) ---"
        )

        session.delete(usuario_db)
        session.commit()

        # Verificamos que ya no existe
        comprobacion = session.execute(select(User)).scalars().all()
        if not comprobacion:
            log.info(f"El usuario con ID {usuario1.id} fue borrado.")


# 3. Funcion Principal
if __name__ == "__main__":
    try:
        ejecutar_crud_demo()
    except Exception as e:  # noqa: BLE001
        log.error(f"Ha ocurrido un error en: {e}")
