from typing import Any

import orjson
from asyncpg.pgproto.pgproto import UUID
from starlette.responses import JSONResponse
UUID

class CusomORJSONResponse(JSONResponse):
    """
    JSON response using the high-performance orjson library to serialize data to JSON.

    Read more about it in the
    [FastAPI docs for Custom Response - HTML, Stream, File, others](https://fastapi.tiangolo.com/advanced/custom-response/).
    """

    def render(self, content: Any) -> bytes:
        assert orjson is not None, "orjson must be installed to use ORJSONResponse"
        return orjson.dumps(
            content, option=orjson.OPT_NON_STR_KEYS | orjson.OPT_SERIALIZE_NUMPY, default=default
        )



def default(obj: Any) -> Any:
    if isinstance(obj, UUID):
        return str(obj)
    raise TypeError("Object is unserializable")