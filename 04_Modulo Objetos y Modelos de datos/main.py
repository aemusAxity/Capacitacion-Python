import json
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import Literal, Protocol, TypedDict

from pydantic import BaseModel, Field, ValidationError

# 0. Typedict y Protocol


# TypeDict programar sin errores tipográficos
class DatosOrden(TypedDict):
    producto: str
    cantidad: int | str  # Union: Puede venir como entero o como string
    precio_unitario: float
    cliente: str


# Protocol definimos un contrato.
# Cualquier objeto que tenga un método '.total' se considerará un "Calculable".
class Calculable(Protocol):
    @property
    def total(self) -> float: ...


# 1. Modelo Pydantic de validacion


class OrderIn(BaseModel):
    producto: str = Field(..., min_length=3, description="Nombre del producto")
    cantidad: int = Field(..., gt=0, description="Debe ser mayor a 0")
    precio_unitario: float = Field(..., ge=0, description="No puede ser negativo")
    cliente: str
    estado: Literal["PENDIENTE", "PAGADO"] = (
        "PENDIENTE"  # Literal el estado solo puede ser una de esas dos
    )


class OrderOut(BaseModel):
    id_orden: str
    producto: str
    total: float
    fecha: datetime
    estado: str


# 2. Entidad de negocio (dataclass)


@dataclass
class Order:
    producto: str
    cantidad: int
    precio_unitario: float
    cliente: str
    estado: Literal["PENDIENTE", "PAGADO"]

    id_orden: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    fecha: datetime = field(default_factory=datetime.now)

    @property
    def total(self) -> float:  # Devuelve un float
        return self.cantidad * self.precio_unitario

    def __str__(self) -> str:  # Devuelve un string
        return f"Orden [{self.id_orden}] - {self.producto} x{self.cantidad} (${self.total})"

    # Comparamos contra Any, porque podríamos intentar compararlo con un int u otro objeto por error
    def __eq__(self, otra_orden: object) -> bool:  # Devuelve un booleano
        if not isinstance(otra_orden, Order):
            return False
        return (
            self.cliente == otra_orden.cliente and self.producto == otra_orden.producto
        )


# 3. Funciones auxuliares
# Se usa el TypedDict 'DatosOrden'
def leer_archivo_json(ruta_archivo: str) -> DatosOrden:
    with open(ruta_archivo, "r", encoding="utf-8") as archivo:
        datos: DatosOrden = json.load(archivo)
        return datos


# Se usa Protocol 'Calculable'
def imprimir_impuestos(objeto: Calculable) -> None:
    impuesto = objeto.total * 0.16
    print(f"IVA (16%): ${impuesto:.2f}")


def procesar_orden(datos: DatosOrden) -> OrderOut:
    datos_limpios = OrderIn(**datos)  # type: ignore[arg-type]
    orden_interna = Order(**datos_limpios.model_dump())

    # Llamamos a nuestra función de Protocolo
    imprimir_impuestos(orden_interna)

    ticket = OrderOut(
        id_orden=orden_interna.id_orden,
        producto=orden_interna.producto,
        total=orden_interna.total,
        fecha=orden_interna.fecha,
        estado=orden_interna.estado,
    )
    return ticket


# 4. Función principal
if __name__ == "__main__":
    arch_json = "pedidos.json"
    print("PASO 1: Leyendo archivo 'pedidos.json'...")
    try:
        datos_json = leer_archivo_json(arch_json)
        print(f"Datos leídos: {datos_json}\n")

        print(
            "PASO 2, 3 y 4: Validando (Pydantic), Procesando (Dataclass) y Generando Ticket..."
        )
        ticket = procesar_orden(datos_json)

        # Imprimimos el ticket de salida
        print("\nTicket generado:")
        print("-" * 30)
        print(f"ID del Pedido : {ticket.id_orden}")
        print(f"Producto      : {ticket.producto}")
        print(f"Total a Pagar : ${ticket.total}")
        print(f"Estado        : {ticket.estado}")
        print(f"Fecha         : {ticket.fecha.strftime('%Y-%m-%d %H:%M:%S')}")
        print("-" * 30)

    except FileNotFoundError:
        print(
            "Error: No se encontró el archivo 'pedidos.json'. Asegúrate de crearlo en esta carpeta."
        )
    except json.JSONDecodeError:
        print("Error: El archivo 'pedido.json' no tiene un formato válido.")
    except ValidationError as e:
        print("\nALERTA: El JSON tiene datos inválidos según nuestras reglas.")
        print(e)
