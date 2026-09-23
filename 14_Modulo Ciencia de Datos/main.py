import csv
import logging
from pathlib import Path

import joblib
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

# Herramientas de Machine Learning
from sklearn.tree import DecisionTreeClassifier

# NOTA: Se hizo omisión al uso de pandas debido a problemas de administrador de la computadora

# 0. Config. del Logger

carpeta_logs = Path("logs")
carpeta_logs.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(carpeta_logs / "modelo.log", encoding="utf-8"),
        logging.StreamHandler(),
    ],
)
log = logging.getLogger(__name__)

RUTA_CSV = Path("data/clientes.csv")
RUTA_MODELO = Path("data/modelo_arbol.pkl")


# Fase 1 Entrenando el modelo
def entrenar_modelo() -> None:
    log.info("--- FASE 1: Entrenamiento ---")

    # 1. Cargar y limpiar los datos
    log.info("1. Cargando datos desde CSV...")

    X_lista = []
    y_lista = []

    with open(RUTA_CSV, mode="r", encoding="utf-8") as archivo:
        lector = csv.DictReader(archivo)
        for fila in lector:
            # Limpiamos filas que tengan espacios vacíos (como la fila 4 de nuestro CSV)
            if (
                not fila["edad"].strip()
                or not fila["salario"].strip()
                or not fila["compro_producto"].strip()
            ):
                continue
            X_lista.append([int(fila["edad"]), int(fila["salario"])])
            y_lista.append(int(fila["compro_producto"]))

    log.info(f"   Datos limpios: {len(X_lista)} filas disponibles.")

    # 2. Se separan los datos (X = Preguntas, y = Respuestas correctas)
    X = X_lista  # Las características del cliente
    y = y_lista  # Lo que queremos adivinar (1=Sí, 0=No)

    # 80% train, 20% test
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # 3. Entrenar el clasificador (árbol de decisión)
    log.info("2. Entrenando el cerebro matemático (Árbol de Decisión)...")
    modelo = DecisionTreeClassifier()
    modelo.fit(X_train, y_train)  # Aquí aprende

    # 4. Evaluar modelo
    predicciones_test = modelo.predict(X_test)
    calificacion = accuracy_score(y_test, predicciones_test)
    log.info(f"   Precisión del modelo en el test: {calificacion * 100}%")

    # 5. Serialización congelar y guardar el modelo
    log.info(f"3. Guardando el modelo entrenado en: {RUTA_MODELO}")
    joblib.dump(modelo, RUTA_MODELO)


# Fase 2 Inferencia básica


def probar_inferencia(edad: int, salario: int) -> None:
    log.info("\n--- FASE 2: Inferencia (Predicción) ---")

    if not RUTA_MODELO.exists():
        log.error("No se encuentra el modelo entrena primero.")
        return

    # 1. Cargar el modelo gaurdado
    modelo_cargado = joblib.load(RUTA_MODELO)

    # 2. Preparar los datos nuevos (Debe tener la misma estructura que Pandas)
    nuevo_cliente = [[edad, salario]]

    # 3. Hacer la inferencia (adivinar)
    prediccion = modelo_cargado.predict(nuevo_cliente)

    resultado = "Si comprara" if prediccion[0] == 1 else "No comprará"
    log.info(
        f"Predicción para un cliente de {edad} años ganando ${salario}: {resultado}"
    )


# Funcion principal

if __name__ == "__main__":
    # Creamos la carpeta de datos si no existe
    Path("data").mkdir(exist_ok=True)

    # Solo corremos el entrenamiento si el archivo no existe (simulando vida real)
    if not RUTA_MODELO.exists():
        entrenar_modelo()
    else:
        log.info("El modelo ya estaba entrenado, saltando Fase 1.")

    # Probamos a un joven sin mucho dinero
    probar_inferencia(edad=19, salario=18000)

    # Probamos a un adulto con buen salario
    probar_inferencia(edad=42, salario=85000)
