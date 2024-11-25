import logging

import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from api import router

app = FastAPI(title="Auth Service API")


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

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router.router)

add_pagination(app)

if __name__ == "__main__":
    log_config = uvicorn.config.LOGGING_CONFIG
    log_config["formatters"]["access"]["fmt"] = "%(asctime)s - %(levelname)s - %(message)s"
    log_config["formatters"]["default"]["fmt"] = "%(asctime)s - %(levelname)s - %(message)s"

    uvicorn.run("main:app", host="0.0.0.0", port=8002, reload=True, log_level="info", log_config=log_config)
