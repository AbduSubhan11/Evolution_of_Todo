import logging
from logging.handlers import RotatingFileHandler
import os
from datetime import datetime

# Create logs directory if it doesn't exist
os.makedirs("logs", exist_ok=True)

# Configure logging
def setup_logging():
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Create logger
    logger = logging.getLogger("todo_api")
    logger.setLevel(logging.INFO)

    # Create file handler with rotation
    file_handler = RotatingFileHandler(
        "logs/todo_api.log",
        maxBytes=1024*1024*10,  # 10MB
        backupCount=5
    )
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    # Add handlers to logger
    if not logger.handlers:
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger

# Global logger instance
logger = setup_logging()

def log_authentication_event(event_type: str, user_id: str = None, details: dict = None):
    """Log authentication-related events"""
    log_msg = f"AUTH_EVENT - Type: {event_type}"
    if user_id:
        log_msg += f", UserID: {user_id}"
    if details:
        log_msg += f", Details: {details}"

    logger.info(log_msg)

def log_task_operation(operation: str, user_id: str, task_id: str = None, details: dict = None):
    """Log task-related operations"""
    log_msg = f"TASK_OPERATION - Operation: {operation}, UserID: {user_id}"
    if task_id:
        log_msg += f", TaskID: {task_id}"
    if details:
        log_msg += f", Details: {details}"

    logger.info(log_msg)

def log_error(error_msg: str, context: dict = None):
    """Log error events"""
    log_msg = f"ERROR - {error_msg}"
    if context:
        log_msg += f", Context: {context}"

    logger.error(log_msg)

def log_api_request(endpoint: str, method: str, user_id: str = None, ip_address: str = None):
    """Log API requests"""
    log_msg = f"API_REQUEST - {method} {endpoint}"
    if user_id:
        log_msg += f", UserID: {user_id}"
    if ip_address:
        log_msg += f", IP: {ip_address}"

    logger.info(log_msg)