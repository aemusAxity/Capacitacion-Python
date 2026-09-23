import asyncio
import logging
import time
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import httpx

# 0. Config. del Logger

carpeta_logs = Path("logs")
carpeta_logs.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,  # Lo dejamos en INFO para no saturar la consola con mensajes de httpx
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(carpeta_logs / "rendimiento.log", encoding="utf-8"),
        logging.StreamHandler(),
    ],
)
log = logging.getLogger(__name__)

# Usaremos un "retraso" de 1 segundo en el servidor para medir la diferencia real
URL_BASE = "https://httpbin.org/delay/1"
TOTAL_PETICIONES = 5


# 1. Modo síncrono
# Hace 5 peticiones de 1 seg cada una. Espera a que termine una para iniciar otra
def fetcher_sincrono():
    log.info("Iniciando descarga Síncrona (Una por una)...")

    with httpx.Client(timeout=10.0) as cliente:
        for i in range(TOTAL_PETICIONES):
            cliente.get(URL_BASE)


# 2. Modo asíncrono (Asyncio + Httpx + Semáforo)

semaforo = asyncio.Semaphore(3)


async def hacer_peticion(cliente: httpx.AsyncClient, numero: int):
    # Petición individual asíncrona
    async with semaforo:
        await cliente.get(URL_BASE)


async def fetcher_asincrono():
    # Dispara las peticiones al mismo tiempo (Controladas por el semáforo)
    log.info("Iniciando descarga Asíncrona (Concurrente)...")

    async with httpx.AsyncClient(timeout=10.0) as cliente:
        tareas = [hacer_peticion(cliente, i) for i in range(TOTAL_PETICIONES)]
        await asyncio.gather(*tareas)


# 3. CPU-Bound Multiproccesing (Para matemáticas pesadas)
# Simula una tarea que ahoga el procesador (Evade el GIL)
def calculo_pesado(numero: int) -> int:
    resultado = 0
    for i in range(numero * 1000000):
        resultado += i
    return resultado


# Usa todos los núcleos del procesador de la PC a la vez
def ejecutar_multiprocesamiento():
    log.info("Iniciando cálculo CPU-bound con Multiprocessing...")

    numeros_a_calcular = [20, 20, 20, 20]

    with ProcessPoolExecutor() as ejecutor:
        list(ejecutor.map(calculo_pesado, numeros_a_calcular))


# 4. Cronómetro


def medir_tiempo(funcion, es_asincrona=False):
    inicio = time.perf_counter()

    if es_asincrona:
        asyncio.run(funcion())
    else:
        funcion()

    fin = time.perf_counter()
    log.info(f"Tiempo exacto: {fin - inicio:.2f} segundos\n")


if __name__ == "__main__":

    # Medir Síncrono
    medir_tiempo(fetcher_sincrono)

    # Medir Asíncrono
    medir_tiempo(fetcher_asincrono, es_asincrona=True)

    # Medir multiprocessing
    medir_tiempo(ejecutar_multiprocesamiento)
