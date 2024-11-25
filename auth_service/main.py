import logging
import sys
import traceback
import uuid
from contextlib import asynccontextmanager
from typing import Callable, AsyncGenerator

from fastapi.encoders import jsonable_encoder
from fastapi_users import FastAPIUsers

import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import JSONResponse

from api.user import router
from config.exceptions import to_dict

from config.orjson import CusomORJSONResponse
from models.user import User
from repositories.auth import get_user_manager
from schemas.users import UserReadSchema, UserCreate
from config.jwt_conf import auth_backend

app = FastAPI(title="Auth Service API")
logger = logging.getLogger()


class SecurityMiddleware(BaseHTTPMiddleware):
    async def dispatch(
            self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        if "/docs" not in request.url.path and "/admin" not in request.url.path:
            response = await call_next(request)
            response.headers["x-content-type-options"] = "nosniff"
            response.headers["x-frame-options"] = "deny"
            response.headers["Content-Security-Policy"] = "default-src"
            return response
        else:
            return await call_next(request)


app.add_middleware(SecurityMiddleware)

fastapi_users = FastAPIUsers[User, uuid.UUID](
    get_user_manager,
    [auth_backend],
)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    fastapi_users.get_register_router(UserReadSchema, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(router)


@app.middleware('http')
async def handle_exceptions(request: Request, call_next: Callable) -> Response | CusomORJSONResponse:
    try:
        response = await call_next(request)
        return response
    except Exception:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        tb_str = traceback.format_exception(exc_type, exc_value, exc_traceback)
        full_tb_str = ''.join(tb_str)
        logger.error(f'An error occurred: {exc_value}\n{full_tb_str}')
        json_data = jsonable_encoder(to_dict(message='Server error'))
        return JSONResponse(json_data, status_code=500)


if __name__ == "__main__":
    log_config = uvicorn.config.LOGGING_CONFIG
    log_config["formatters"]["access"]["fmt"] = "%(asctime)s - %(levelname)s - %(message)s"
    log_config["formatters"]["default"]["fmt"] = "%(asctime)s - %(levelname)s - %(message)s"

    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True, log_level="info", log_config=log_config)
