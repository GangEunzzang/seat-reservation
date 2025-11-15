from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from core.exception.domain_exception import DomainException
from core.response.api_response import ApiResponse


def exceptions_handler(app: FastAPI) -> None:
    """Setup all exception handlers"""

    @app.exception_handler(DomainException)
    async def handle_domain_exception(request: Request, exc: DomainException):
        return JSONResponse(
            status_code=exc.status_code,
            content=ApiResponse.error(
                message=exc.message,
                code=exc.error_code.name
            ).model_dump()
        )

    @app.exception_handler(StarletteHTTPException)
    async def handle_http_exception(request: Request, exc: StarletteHTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content=ApiResponse.error(
                message=str(exc.detail),
                code=f"HTTP_{exc.status_code}"
            ).model_dump()
        )

    @app.exception_handler(RequestValidationError)
    async def handle_validation_exception(request: Request, exc: RequestValidationError):
        errors = exc.errors()
        error_messages = []
        for err in errors:
            field = ".".join(str(loc) for loc in err["loc"])
            error_messages.append(f"{field}: {err['msg']}")

        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=ApiResponse.error(
                message="; ".join(error_messages),
                code="VALIDATION_ERROR"
            ).model_dump()
        )

    @app.exception_handler(ValueError)
    async def handle_value_error(request: Request, exc: ValueError):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=ApiResponse.error(
                message=str(exc),
                code="VALUE_ERROR"
            ).model_dump()
        )

    @app.exception_handler(Exception)
    async def handle_generic_exception(request: Request, exc: Exception):
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=ApiResponse.error(
                message="Internal server error",
                code="INTERNAL_ERROR"
            ).model_dump()
        )
