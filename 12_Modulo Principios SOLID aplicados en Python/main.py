from typing import Protocol

from pydantic import BaseModel

# 1 Modelos Pydantic
# (SRP: Su única responsabilidad es definir y validar la estructura de datos)


class Orden(BaseModel):
    id: int
    producto: str
    total: float


# 2 Protocol
# (DIP: Inversión de Dependencias y ISP: Segregación de Interfaces)
# Protocolo es nuestro "Contrato".
# Le dice a nuestro sistema: "Cualquier cosa que quiera ser un Repositorio,
# DEBE tener estos dos métodos exactamente con estas firmas".
class RepositorioOrdenes(Protocol):
    def guardar(self, orden: Orden) -> None: ...

    def obtener_todas(self) -> list[Orden]: ...


# 3 Adaptadores / Implementaciones
# (OCP: Si mañana quiero agregar MongoDB, solo creo otra clase nueva sin modificar las existentes)
# (LSP: Ambas clases pueden intercambiarse sin romper el programa)


class RepositorioEnMemoria:
    def __init__(self) -> None:
        self._db: list[Orden] = []

    def guardar(self, orden: Orden) -> None:
        self._db.append(orden)
        print(f"(Memoria) Orden {orden.id} guardada en una simple lista.")
        print(f"(Memoria) La orden completa es: {orden}")

    def obtener_todas(self) -> list[Orden]:
        return self._db


# Simula una base de datos SQL
class RepositorioSQLFalso:
    def __init__(self, string_conexion: str) -> None:
        self.conexion = string_conexion

    def guardar(self, orden: Orden) -> None:
        print(f"(SQL) Ejecutando 'INSERT INTO orders...' para la orden {orden.id}")

    def obtener_todas(self) -> list[Orden]:
        print("(SQL) Ejecutando 'SELECT * FROM orders'")
        return [Orden(id=99, producto="Producto de BD Falsa", total=0.0)]


# 4. La lógica del negocio (el servicio)
# (DIP: Recibe la abstracción RepositorioOrdenes)


class ServicioProcesamientoOrdenes:
    # Inyección de Dependencias
    def __init__(self, repositorio: RepositorioOrdenes) -> None:
        self.repo = repositorio

    def procesar_nueva_orden(self, nueva_orden: Orden) -> None:
        if nueva_orden.total <= 0:
            raise ValueError("El total debe ser mayor a 0")
        print(
            f"(Servicio) Procesando: {nueva_orden.producto} (Total: ${nueva_orden.total})"
        )

        # Guardamos la orden usando la abstracción.
        # Al servicio le da igual si se guarda en RAM o en SQL.
        self.repo.guardar(nueva_orden)


# 5. Funcion Principal

if __name__ == "__main__":

    orden_prueba = Orden(id=1, producto="Laptop", total=1200.0)

    print("--- Ejecutando con Repositorio en Memoria ---")
    repo_memoria = RepositorioEnMemoria()
    # Inyectamos el repositorio en memoria al servicio
    servicio_test = ServicioProcesamientoOrdenes(repositorio=repo_memoria)

    # Le pasamos el objeto Orden validado
    servicio_test.procesar_nueva_orden(orden_prueba)

    print("\n--- Ejecutando con Repositorio SQL ---")
    repo_sql = RepositorioSQLFalso("sqlite:///mi_base.db")
    servicio_prod = ServicioProcesamientoOrdenes(repositorio=repo_sql)

    # Le pasamos el objeto Orden validado
    servicio_prod.procesar_nueva_orden(orden_prueba)
