import grpc
import orders_pb2
import orders_pb2_grpc


def correr_cliente():
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = orders_pb2_grpc.OrderServiceStub(channel)

        orden = orders_pb2.OrderRequest(id_orden="100", cliente="Leila", total=189.99)

        print("Enviando orden vía gRPC...")
        respuesta = stub.CreateOrder(orden)

    print(f"Respuesta: {respuesta.mensaje}")


if __name__ == "__main__":
    correr_cliente()
