import grpc, asyncio
from grpc.aio import ServicerContext
import protobuf.users.users_service_pb2_grpc as users_service_pb2_grpc
from protobuf.users.users_service_pb2 import (
    AddGameToUserRequest,
    AddGameToUserResponse,
    HasGameRequest,
    HasGameResponse,
)


class UsersServiceServicer(users_service_pb2_grpc.PaymentServiceServicer):
    async def AddGameToUser(
        self,
        request: AddGameToUserRequest,
        context: ServicerContext
    ) -> AddGameToUserResponse:
        ...

    async def HasGame(
        self,
        request: HasGameRequest,
        context: ServicerContext
    ) -> HasGameResponse:
        ...

async def serve():
    server = grpc.aio.server()
    users_service_pb2_grpc.add_UserServiceServicer_to_server(UsersServiceServicer(), server)
    server.add_insecure_port('[::]:8002')

    await server.start()
    await server.wait_for_termination()
    await server.stop(grace=5)

if __name__ == "__main__":
    asyncio.run(serve())