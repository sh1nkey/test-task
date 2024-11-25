from uuid import UUID

import grpc
from fastapi import Header, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from google.protobuf.json_format import MessageToDict

from protos.pb import auth_pb2_grpc, auth_pb2

from utils_types import UserDict

auth_scheme = HTTPBearer()


async def get_current_user(auth: HTTPAuthorizationCredentials = Depends(auth_scheme)) -> UserDict:
    return await get_user(auth.credentials)


async def get_user(token: UUID | str) -> UserDict:
    async with grpc.aio.insecure_channel("localhost:50051") as channel:
        stub = auth_pb2_grpc.AuthServiceStub(channel)
        response = await stub.GetUser(auth_pb2.AuthRequest(token=token))

    return MessageToDict(
        response,
        preserving_proto_field_name=True,
        use_integers_for_enums=False,
    )


async def check_recipient_exists(id: str):
    async with grpc.aio.insecure_channel("localhost:50051") as channel:
        stub = auth_pb2_grpc.CheckUserServiceStub(channel)
        response = await stub.CheckUser(auth_pb2.CheckUserRequest(id=str(id)))

    return MessageToDict(
        response,
        preserving_proto_field_name=True,
        use_integers_for_enums=False,
    )
