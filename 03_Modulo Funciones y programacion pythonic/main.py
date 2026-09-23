import random
import time


# 1. CONTEXT MANAGER: Mide el tiempo de ejecución de un bloque de código
class Temporizador:
    def __enter__(self):
        # Lo que pasa al entrar al bloque 'with'
        self.inicio = time.time()
        print("Inicio tarea")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Lo que pasa al salir del bloque 'with' (incluso si hubo error)
        fin = time.time()
        print(f"Tarea finalizada. Tiempo total: {fin - self.inicio:.4f} segundos\n")
        # Si devolvemos False, las excepciones se propagan. Si devolvemos True, se silencian.
        return False


# 2. DECORADOR: Reintentos con backoff exponencial
def reintentar_con_backoff(max_intentos, espera_inicial):
    def decorador(funcion):
        def envoltura(*args, **kwargs):
            intentos = 0
            espera = espera_inicial

            while intentos < max_intentos:
                try:
                    return funcion(*args, **kwargs)  # Intentamos ejecutar la función
                except Exception as e:
                    intentos += 1
                    if intentos == max_intentos:
                        print(f"Fallo tras {max_intentos} intentos. Error final: {e}")
                        raise  # Rendirse y lanzar el error
                    print(
                        f"Intento # {intentos} falló: {e}. Reintentando en {espera}s..."
                    )
                    time.sleep(espera)
                    espera *= 2  # Multiplicar el tiempo de espera (backoff)

        return envoltura

    return decorador


# 3. GENERADOR: Procesar listas grandes en lotes pequeños (batches)
def generador_lotes(lista_datos, tam_lote):
    # Usamos range para saltar de lote en lote
    for i in range(0, len(lista_datos), tam_lote):
        # yield pausa la función aquí y devuelve este "pedacito"
        yield lista_datos[i : i + tam_lote]


# --- SIMULANDO LA OPERACIÓN ---


# Aplicamos nuestro decorador a esta función
@reintentar_con_backoff(max_intentos=3, espera_inicial=1)
def procesar_lote_en_api(lote):
    # Simulamos que el 30% de las veces la API falla "por red"
    if random.random() < 0.3:
        raise ConnectionError("¡Caída de red aleatoria!")

    print(f"Lote enviado exitosamente: {lote}")
    return True


# Bloque principal de ejecución
if __name__ == "__main__":
    datos_gigantes = list(range(1, 21))  # Simulamos 20 registros

    # Usamos el Context Manager con la palabra 'with'
    with Temporizador():
        # Usamos el Generador en un for (lotes de 5)
        for lote in generador_lotes(datos_gigantes, tam_lote=5):
            print(f"Procesando lote: {lote}")
            # Llamamos a la función decorada
            procesar_lote_en_api(lote)
