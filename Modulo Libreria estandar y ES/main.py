import csv
import json
import logging
from datetime import datetime, timezone
from pathlib import Path

# 0. Estructura de carpetas

# Creamos las carpetas antes de configurar, por si no existen.
carpeta_logs = Path("logs")
carpeta_data = Path("data")

carpeta_logs.mkdir(exist_ok=True)
carpeta_data.mkdir(exist_ok=True)

# 1. Configurar logging

log = logging.getLogger("LabLogger")
log.setLevel(logging.DEBUG)

formato = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

# Archivo de destino en la carpeta 'logs'
archivo_log = Path("logs/sistema.log")
archivo_handler = logging.FileHandler(archivo_log, encoding="utf-8")
archivo_handler.setFormatter(formato)

# Consola de destino
consola_handler = logging.StreamHandler()
consola_handler.setFormatter(formato)

# Agregamos los manejadores (handlers) al logger
log.addHandler(archivo_handler)
log.addHandler(consola_handler)


# 2. Procesamiento (E/S)


def procesar_ventas(ruta_csv: Path) -> dict[str, object]:
    log.info("Leyendo archivo")

    if not ruta_csv.exists():
        log.critical(f"El archivo {ruta_csv} no existe.")
        raise FileNotFoundError(f"Falta archivo: {ruta_csv}")

    total_ingresos = 0.0
    conteo_productos: dict[str, int] = {}

    with ruta_csv.open(mode="r", encoding="utf-8") as archivo:
        lector = csv.DictReader(archivo)

        for fila in lector:
            try:
                producto = fila["producto"]
                cantidad = int(fila["cantidad"])
                precio = float(fila["precio"])

                # Cálculo de métricas
                total_ingresos += cantidad * precio
                conteo_productos[producto] = (
                    conteo_productos.get(producto, 0) + cantidad
                )

                log.debug(f"Fila procesada: {producto}")

            except (KeyError, ValueError, TypeError) as e:
                log.warning(f"Una fila ha sido ignorada: {fila}. Razón: {e}")

    log.info("Lectura de CSV finalizado con éxito.")

    return {
        "ingresos_totales": round(total_ingresos, 2),
        "productos_vendidos": conteo_productos,
        "generado": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
    }


# 3. Exportar en JSON


def guardar_reporte(datos: dict[str, object], ruta_json: Path) -> None:
    log.info("Guardando métricas en metricas.json")
    with ruta_json.open(mode="w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, indent=4)
    log.info("Exportación completa")


# 4. Funcion principal

if __name__ == "__main__":
    csv_entrada = Path("data/ventas.csv")
    json_salida = Path("data/metricas.json")

    try:
        metricas = procesar_ventas(csv_entrada)
        guardar_reporte(metricas, json_salida)
    except Exception as e:  # noqa: BLE001
        log.error(f"Error en la ejecución principal: {e}")
