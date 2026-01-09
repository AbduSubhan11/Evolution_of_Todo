from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from typing import Dict, Any


class APIError(Exception):
    """Base exception class for API errors"""
    def __init__(self, code: str, message: str, details: str = None, status_code: int = 500):
        self.code = code
        self.message = message
        self.details = details
        self.status_code = status_code
        super().__init__(self.message)


async def http_exception_handler(request: Request, exc: HTTPException):
    """Global handler for HTTP exceptions"""
    error_code_map = {
        400: "VALIDATION_ERROR",
        401: "UNAUTHORIZED",
        403: "FORBIDDEN",
        404: "NOT_FOUND",
        409: "CONFLICT",
        500: "INTERNAL_ERROR"
    }

    error_code = error_code_map.get(exc.status_code, "HTTP_ERROR")

    error_response = {
        "error": {
            "code": error_code,
            "message": exc.detail,
        }
    }

    # Add details only if they exist
    if exc.detail and exc.detail != str(exc.status_code):
        error_response["error"]["details"] = str(exc.detail)

    return JSONResponse(
        status_code=exc.status_code,
        content=error_response
    )


async def api_exception_handler(request: Request, exc: APIError):
    """Global handler for API errors"""
    error_response = {
        "error": {
            "code": exc.code,
            "message": exc.message
        }
    }

    if exc.details:
        error_response["error"]["details"] = exc.details

    return JSONResponse(
        status_code=exc.status_code,
        content=error_response
    )


async def validation_exception_handler(request: Request, exc: Exception):
    """Global handler for validation errors"""
    error_response = {
        "error": {
            "code": "VALIDATION_ERROR",
            "message": "Request validation failed"
        }
    }

    # Add details if available
    if str(exc):
        error_response["error"]["details"] = str(exc)

    return JSONResponse(
        status_code=400,
        content=error_response
    )


async def general_exception_handler(request: Request, exc: Exception):
    """Global handler for unexpected errors"""
    error_response = {
        "error": {
            "code": "INTERNAL_ERROR",
            "message": "An internal server error occurred"
        }
    }

    # Add details only in development
    if str(exc) and __name__ == "__main__":
        error_response["error"]["details"] = str(exc)

    return JSONResponse(
        status_code=500,
        content=error_response
    )


def add_global_exception_handlers(app):
    """Add global exception handlers to the FastAPI app"""
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(APIError, api_exception_handler)
    app.add_exception_handler(Exception, general_exception_handler)

    return app