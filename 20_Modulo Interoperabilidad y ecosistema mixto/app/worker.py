import redis

# Worker escucha los eventos, es quien hace el trabajo
# pesado (enviar correos, actualizar inventarios, generar PDF de la factura).


def iniciar_worker():
    redis_client = redis.Redis(host="localhost", port=6379, db=0)
    pubsub = redis_client.pubsub()
    pubsub.subscribe("canal_ordenes")

    print("[Worker] Escuchando eventos en Redis...")

    for mensaje in pubsub.listen():
        if mensaje["type"] == "message":
            datos = mensaje["data"].decode("utf-8")
            print(f"[Worker] Evento procesado: Enviando email para {datos}")


if __name__ == "__main__":
    iniciar_worker()
