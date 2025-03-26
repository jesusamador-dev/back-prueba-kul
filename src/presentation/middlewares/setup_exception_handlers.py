from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError


def setup_exception_handlers(app):
    @app.exception_handler(RequestValidationError)
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        errors = exc.errors()
        simplified_errors: list = []

        for error in errors:
            simplified_errors.append({
                "detail": error["msg"].replace("Value error, ", ""),
                "key": error["loc"][-1],
            })

        return JSONResponse(
            status_code=422,
            content={"errors": simplified_errors}
        )

    @app.exception_handler(ValueError)
    async def value_error_handler(request: Request, exc: ValueError):
        return JSONResponse(
            status_code=400,
            content={"error": str(exc)}
        )