from concurrent import futures

import grpc
import orders_pb2
import orders_pb2_grpc
import redis

# Server, recibe la petición de client.py

redis_client = redis.Redis(host="localhost", port=6379, db=0)


class OrderServicer(orders_pb2_grpc.OrderServiceServicer):
    def CreateOrder(self, request, context):
        print(f"[Servidor gRPC] Orden {request.id_orden} recibida.")

        # Publicamos el evento a Redis
        mensaje = f"NUEVA_ORDEN: {request.id_orden} {request.cliente}"
        redis_client.publish("canal_ordenes", mensaje)

        return orders_pb2.OrderResponse(
            mensaje=f"Orden creada para {request.cliente}. Procesando en background.",
            exito=True,
        )


def serve():
    # Levantamos un servidor gRPC con 10 "hilos" de trabajo
    # gRPC usa el puerto por defecto usa 50051
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    orders_pb2_grpc.add_OrderServiceServicer_to_server(OrderServicer(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    print("Servidor gRPC encendido (Puerto 50051).")
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
