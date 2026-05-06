from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StartletteHTTPException

from app.exceptions.exceptions import BaseCustomException


def custom_base_exception_handler(request: Request, exc):
    succesfull: bool = False
    content: dict = {"succesfull": succesfull, "message": exc.detail}
    return JSONResponse(status_code=exc.status_code, content=content)


def custom_exception_handler(request: Request, exc):
    content: dict = {"message": exc.detail}
    return JSONResponse(status_code=exc.status_code, content=content)


def register_handlers(app: FastAPI):
    app.add_exception_handler(BaseCustomException, custom_base_exception_handler)
    app.add_exception_handler(StartletteHTTPException, custom_exception_handler)
