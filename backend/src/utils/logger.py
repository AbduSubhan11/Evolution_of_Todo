import logging
import sys
from datetime import datetime
from typing import Any, Dict
import json


class CustomFormatter(logging.Formatter):
    """
    Custom formatter to add extra context to log messages
    """
    def format(self, record):
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }

        # Add extra fields if they exist
        if hasattr(record, 'user_id'):
            log_entry['user_id'] = record.user_id
        if hasattr(record, 'request_id'):
            log_entry['request_id'] = record.request_id
        if hasattr(record, 'conversation_id'):
            log_entry['conversation_id'] = record.conversation_id

        # Convert to JSON string
        return json.dumps(log_entry)


def setup_logger(name: str = __name__, level: int = logging.INFO) -> logging.Logger:
    """
    Set up a logger with custom formatting
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Prevent duplicate handlers
    if logger.handlers:
        return logger

    # Create handler
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(level)

    # Create formatter
    formatter = CustomFormatter()
    handler.setFormatter(formatter)

    # Add handler to logger
    logger.addHandler(handler)

    return logger


def log_ai_interaction(user_id: str, conversation_id: str, input_message: str, output_message: str, tools_used: list = None):
    """
    Log AI interaction for monitoring and debugging
    """
    logger = setup_logger("ai_interaction")

    logger.info("AI Interaction", extra={
        "user_id": user_id,
        "conversation_id": conversation_id,
        "input": input_message,
        "output": output_message,
        "tools_used": tools_used or [],
        "interaction_type": "ai_chat"
    })


def log_tool_execution(user_id: str, conversation_id: str, tool_name: str, input_params: dict, result: dict):
    """
    Log tool execution for monitoring and debugging
    """
    logger = setup_logger("tool_execution")

    logger.info("Tool Execution", extra={
        "user_id": user_id,
        "conversation_id": conversation_id,
        "tool_name": tool_name,
        "input_params": input_params,
        "result": result,
        "execution_status": result.get("success", "unknown")
    })


def log_error(error: Exception, context: str = "", user_id: str = None):
    """
    Log errors with context
    """
    logger = setup_logger("errors")

    extra = {"context": context}
    if user_id:
        extra["user_id"] = user_id

    logger.error(f"{str(error)}", extra=extra)


def log_api_request(endpoint: str, method: str, user_id: str = None, duration_ms: float = None):
    """
    Log API requests for monitoring
    """
    logger = setup_logger("api_requests")

    extra = {
        "endpoint": endpoint,
        "method": method,
        "duration_ms": duration_ms
    }
    if user_id:
        extra["user_id"] = user_id

    logger.info("API Request", extra=extra)


# Pre-configured loggers for different purposes
ai_logger = setup_logger("ai_interaction")
tool_logger = setup_logger("tool_execution")
api_logger = setup_logger("api_requests")
error_logger = setup_logger("errors")