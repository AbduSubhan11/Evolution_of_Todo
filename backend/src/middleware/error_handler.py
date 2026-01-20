from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
import traceback
import logging

# Set up logger
logger = logging.getLogger(__name__)


async def global_exception_handler(request: Request, exc: Exception):
    """
    Global exception handler for the application
    """
    # Log the error with traceback
    logger.error(f"Unhandled exception occurred: {exc}\nTraceback: {traceback.format_exc()}")

    # Return appropriate error response based on exception type
    if isinstance(exc, HTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": exc.detail,
                "status": "error"
            }
        )
    elif isinstance(exc, RequestValidationError):
        return JSONResponse(
            status_code=422,
            content={
                "error": "Validation error",
                "details": exc.errors(),
                "status": "error"
            }
        )
    else:
        # For unexpected errors, return a generic error message
        return JSONResponse(
            status_code=500,
            content={
                "error": "An internal server error occurred",
                "status": "error"
            }
        )


async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """
    Handler for HTTP exceptions
    """
    logger.warning(f"HTTP exception: {exc.status_code} - {exc.detail}")

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "status": "error"
        }
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Handler for validation exceptions
    """
    logger.warning(f"Validation error: {exc.errors()}")

    return JSONResponse(
        status_code=422,
        content={
            "error": "Validation error",
            "details": exc.errors(),
            "status": "error"
        }
    )


def setup_error_handlers(app):
    """
    Register error handlers with the FastAPI app
    """
    app.add_exception_handler(StarletteHTTPException, http_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(Exception, global_exception_handler)