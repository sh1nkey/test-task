import asyncio
import logging

import grpc
from grpc_interceptor.exceptions import GrpcException, NotFound

from protos.pb import auth_pb2_grpc, auth_pb2

from config.jwt_conf import user_ex_token
from config.uow_conf import UnitOfWork
from services.user import UserService


class AuthGreeter(auth_pb2_grpc.AuthServiceServicer):
    async def GetUser(
            self,
            request: auth_pb2.AuthRequest,
            context: grpc.aio.ServicerContext,
    ) -> auth_pb2.AuthResponse:
        grpc_exception = GrpcException(
            details="Что-то не так с декодированием токена",
            status_code=grpc.StatusCode.UNKNOWN,
        )

        user_data = await user_ex_token(request.token, UnitOfWork(), grpc_exception)

        if not user_data:
            raise NotFound(
                details="Пользователь не найден",
                status_code=grpc.StatusCode.NOT_FOUND,
            )
        return auth_pb2.AuthResponse(id=str(user_data["id"]), email=user_data["email"])

    async def CheckUser(
            self,
            request: auth_pb2.CheckUserRequest,
            context: grpc.aio.ServicerContext,
    ) -> auth_pb2.CheckUserResponse:
        print("""asdasdaasdads""")

        user_exists: bool = await UserService.check_exist(UnitOfWork(), request.id)
        if not user_exists:
            raise NotFound(
                details="Drink out of stock",
                status_code=grpc.StatusCode.NOT_FOUND,
            )
        return auth_pb2.CheckUserResponse(exists=user_exists)



class CheckGreeter(auth_pb2_grpc.AuthServiceServicer):

    async def CheckUser(
            self,
            request: auth_pb2.CheckUserRequest,
            context: grpc.aio.ServicerContext,
    ) -> auth_pb2.CheckUserResponse:
        print("""asdasdaasdads""")

        user_exists: bool = await UserService.check_exist(UnitOfWork(), request.id)
        if not user_exists:
            raise NotFound(
                details="Drink out of stock",
                status_code=grpc.StatusCode.NOT_FOUND,
            )
        return auth_pb2.CheckUserResponse(exists=user_exists)


async def serve() -> None:
    server = grpc.aio.server()
    auth_pb2_grpc.add_AuthServiceServicer_to_server(AuthGreeter(), server)
    auth_pb2_grpc.add_CheckUserServiceServicer_to_server(CheckGreeter(), server)

    listen_addr = "0.0.0.0:50051"
    server.add_insecure_port(listen_addr)
    logging.info("Starting server on %s", listen_addr)
    await server.start()
    await server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(serve())
