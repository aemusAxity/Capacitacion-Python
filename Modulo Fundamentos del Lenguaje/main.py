import json


def cargar_datos(ruta_archivo):
    # try: Intentamos abrir el archivo
    try:
        with open(ruta_archivo, "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)
            return datos

    # Si no existe
    except FileNotFoundError:
        print(f"Error: El archivo '{ruta_archivo}' no se encontró.")
        return []

    # Existe pero no es un JSON valido
    except json.JSONDecodeError:
        print("Error: El archivo no tiene un formato JSON válido.")
        return []


mis_datos = cargar_datos("datos.json")


def procesar_registros(registros):
    usuarios_validos = []

    for registro in registros:
        # Pattern Matching (match/case)
        match registro:
            # Caso 1: Estructura exacta de un usuario con nombre y edad numérico
            case {"tipo": "usuario", "nombre": nombre, "edad": int(edad)}:
                print(f"Usuario válido: {nombre}, Edad: {edad}")
                # Agregamos datos (mutamos el diccionario)
                registro["procesado"] = True
                usuarios_validos.append(registro)

            # Caso 2: Es un admin (no nos importa la edad, pero sí el departamento)
            case {"tipo": "admin", "nombre": nombre, "departamento": depto}:
                print(f"Administrador encontrado: {nombre} de {depto}")

            # Caso 3: Es un bot
            case {"tipo": "bot", "nombre": nombre}:
                print(f"Ignorando al bot: {nombre}")

            # Caso por defecto (el comodín '_')
            case _:
                # Aquí caerá 'Beto', porque su edad no es un 'int', sino un string.
                print(
                    f"Error de formato en registro: {registro.get('nombre', 'Desconocido')}"
                )

    return usuarios_validos


# Ejecutamos el procesamiento
if mis_datos:
    print("\n--- Iniciando procesamiento ---")
    resultados = procesar_registros(mis_datos)
    print("\n--- Resultados (Usuarios procesados) ---")
    print(resultados)
