import json
import logging
from pathlib import Path

import httpx
from tenacity import retry, stop_after_attempt

# 0. Configurar logger y carpetas

carpeta_logs = Path("logs")
carpeta_data = Path("API")

carpeta_logs.mkdir(exist_ok=True)
carpeta_data.mkdir(exist_ok=True)

log = logging.getLogger("APILogger")
log.setLevel(logging.DEBUG)

formato = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

archivo_log = carpeta_logs / "sistema.log"
archivo_handler = logging.FileHandler(archivo_log, encoding="utf-8")
archivo_handler.setFormatter(formato)

# Consola
consola_handler = logging.StreamHandler()
consola_handler.setFormatter(formato)

log.addHandler(archivo_handler)
log.addHandler(consola_handler)

# 1. Cliente con Timeuts y reintentos


# @retry Si falla reitnenta hasta 3 veces
@retry(stop=stop_after_attempt(3))
def pedir_datos_seguros(url: str, ruta_destino: Path) -> None:
    log.info(f"Solicitando datos a: {url}")

    # timeout=3.0: Si el servidor tarda más de 3 segundos, aborta y lanza error
    respuesta = httpx.get(url, timeout=3.0)
    respuesta.raise_for_status()

    datos = respuesta.json()

    with ruta_destino.open("w", encoding="utf-8") as archivo_local:
        json.dump(datos, archivo_local, indent=4)
        log.info("JSON descargado con exito")


# 2. Descargar por streaming


@retry(stop=stop_after_attempt(3))
def descargar_imagen_streaming(url: str, ruta_destino: Path) -> None:
    log.info(f"Descargando imagen por streaming en: {ruta_destino.name}")

    # Abrimos el archivo en modo "escribir bytes" (wb)
    with (
        ruta_destino.open("wb") as archivo_local,
        # httpx.stream no sobrecarga la RAM
        httpx.stream("GET", url, timeout=10.0) as respuesta,
    ):
        respuesta.raise_for_status()

        # Recibimos la imagen en pedacitos (chunks) y los vamos escribiendo
        for pedazo in respuesta.iter_bytes():
            archivo_local.write(pedazo)

    log.info("Descarga por streaming terminada con éxito.")


# 3. Funcion principal


def main() -> None:
    # URL 1: Forzamos un fallo se simula un servidor que tarda 5 segundos en responder.
    url_lenta = "https://httpbin.org/delay/5"

    # URL 2: Ruta de httpbin que devuelve un JSON básico
    url_json = "https://httpbin.org/get"

    # URL 3: Ruta de httpbin que devuelve una imagen real
    url_imagen = "https://httpbin.org/image/webp"

    ruta_imagen = Path("API/imagen_httpbin.webp")
    ruta_json = Path("API/json_basico.json")

    try:
        pedir_datos_seguros(url_lenta, ruta_json)
    except Exception as e:  # noqa: BLE001
        log.warning(f"Prueba 1 falló tras 3 intentos: {e}")

    try:
        pedir_datos_seguros(url_json, ruta_json)
    except Exception as e:  # noqa: BLE001
        log.error(f"La Prueba 2 falló inesperadamente: {e}")

    try:
        descargar_imagen_streaming(url_imagen, ruta_imagen)
    except Exception as e:  # noqa: BLE001
        log.error(f"Ocurrió un error inesperado al descargar la imagen: {e}")


if __name__ == "__main__":
    main()
