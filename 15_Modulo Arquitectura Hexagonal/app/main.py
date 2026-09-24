from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from app.application.use_cases import CrearOrdenUseCase
from app.infrastructure.repositories import BaseDeDatosEnMemoria


# 1. FastAPI (Infraestructura Web)
# Esto solo sirve para validar el JSON que llega de internet.
class ItemInput(BaseModel):
    nombre: str
    precio: float


class OrderInput(BaseModel):
    id_orden: str
    cliente: str
    items: list[ItemInput]


# 2. Inyeccion de Dependencias
# Instanciamos la BD real (Adaptador de salida)
repositorio_produccion = BaseDeDatosEnMemoria()
# Se la inyectamos al Caso de Uso
caso_de_uso = CrearOrdenUseCase(repositorio=repositorio_produccion)

# 3. Framework web (Adaptador de entrada)
app = FastAPI(title="Sistema de Órdenes con Arq. Hexagonal")


# Adaptador de entrada
# Recibe un HTTP POST, extrae los datos y se los pasa al Caso de Uso.
# FastAPI no sabe de reglas de negocio, solo es un mensajero.
@app.post("/ordenes/")
def crear_orden_endpoint(datos: OrderInput):
    try:
        # Convertimos los datos de Pydantic a una lista de diccionarios normal
        items_dict = [{"nombre": i.nombre, "precio": i.precio} for i in datos.items]

        # Le pasamos el trabajo al Caso de Uso
        orden = caso_de_uso.ejecutar(
            id_orden=datos.id_orden, cliente=datos.cliente, items_data=items_dict
        )

        return {
            "mensaje": "Orden creada con éxito",
            "id": orden.id,
            "total_a_pagar": orden.total,
            "estado": orden.status,
        }

    except ValueError as e:
        # Si el Dominio lanza un error de regla de negocio, podemos dvolver un 400
        raise HTTPException(status_code=400, detail=str(e))
