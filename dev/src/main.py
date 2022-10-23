import time
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.gzip import GZipMiddleware
from data import (
    RepositoryNotConnected,
    RepositoryDuplicateKeyError,
    RepositoryNotFoundError
)
import endpoints


def create_app() -> FastAPI:
    application = FastAPI()
    application.add_middleware(GZipMiddleware, minimum_size=1000)
    application.include_router(endpoints.router)
    return application

app = create_app()


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

# pylint: disable=unused-argument
@app.exception_handler(RepositoryNotConnected)
async def not_connected_handler(request: Request, exc: RepositoryNotConnected):
    return JSONResponse(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        content={"message": "database is currently unavailable"},
    )


# pylint: disable=unused-argument
@app.exception_handler(RepositoryNotFoundError)
async def not_found_handler(request: Request, exc: RepositoryNotFoundError):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"message": "Entity was not found"},
    )

# pylint: disable=unused-argument
@app.exception_handler(RepositoryDuplicateKeyError)
async def duplicate_key_handler(request: Request, exc: RepositoryDuplicateKeyError):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"message": "handle already exists"},
    )
