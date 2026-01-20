from typing import Dict, Any, Optional
from pydantic import BaseModel, validator
import re
import logging

logger = logging.getLogger(__name__)


class SafeContentValidator:
    """
    Validator to ensure content is safe and appropriate
    """
    @staticmethod
    def validate_task_content(content: str) -> bool:
        """
        Validate that task content doesn't contain potentially harmful content
        """
        if not content:
            return True

        # Check for potentially harmful patterns
        harmful_patterns = [
            r"(?i)(system|exec|eval|import|os\.|subprocess).*\(.*\)",  # Code execution
            r"(?i)(drop|delete|truncate|alter|grant|revoke).*table",  # SQL injection
            r"<script.*?>.*?</script>",  # Script tags
            r"javascript:",  # JavaScript URLs
            r"on\w+\s*=",  # Event handlers
        ]

        content_lower = content.lower()
        for pattern in harmful_patterns:
            if re.search(pattern, content_lower):
                logger.warning(f"Potentially harmful content detected: {content[:50]}...")
                return False

        return True

    @staticmethod
    def sanitize_input(text: str) -> str:
        """
        Sanitize input by removing potentially harmful characters/sequences
        """
        if not text:
            return text

        # Remove script tags
        sanitized = re.sub(r'<script[^>]*>.*?</script>', '', text, flags=re.IGNORECASE | re.DOTALL)

        # Remove javascript: urls
        sanitized = re.sub(r'javascript:', '', sanitized, flags=re.IGNORECASE)

        # Remove event handlers
        sanitized = re.sub(r'on\w+\s*=', '', sanitized, flags=re.IGNORECASE)

        return sanitized.strip()


class ChatRequestValidator:
    """
    Validator for chat API requests
    """
    @staticmethod
    def validate_message(message: str) -> Dict[str, Any]:
        """
        Validate a chat message
        """
        errors = []

        if not message or not message.strip():
            errors.append("Message cannot be empty")

        if len(message.strip()) > 10000:  # Max 10k chars
            errors.append("Message is too long (max 10000 characters)")

        if not SafeContentValidator.validate_task_content(message):
            errors.append("Message contains potentially harmful content")

        return {
            "is_valid": len(errors) == 0,
            "errors": errors,
            "sanitized_message": SafeContentValidator.sanitize_input(message) if message else ""
        }

    @staticmethod
    def validate_conversation_id(conversation_id: Optional[str]) -> Dict[str, Any]:
        """
        Validate conversation ID format
        """
        if not conversation_id:
            return {"is_valid": True, "normalized_id": None}

        # Basic UUID format check
        uuid_pattern = r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
        if re.match(uuid_pattern, conversation_id.lower()):
            return {"is_valid": True, "normalized_id": conversation_id}
        else:
            # Might be a custom format, allow it but log for review
            logger.info(f"Non-standard conversation ID format: {conversation_id[:10]}...")
            return {"is_valid": True, "normalized_id": conversation_id}


class TaskOperationValidator:
    """
    Validator for task operations
    """
    @staticmethod
    def validate_add_task_params(params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate parameters for adding a task
        """
        errors = []
        warnings = []

        if "title" not in params or not params["title"] or not str(params["title"]).strip():
            errors.append("Title is required for adding a task")

        if "title" in params:
            title = str(params["title"])
            if len(title) > 200:
                errors.append("Title is too long (max 200 characters)")

            if not SafeContentValidator.validate_task_content(title):
                errors.append("Title contains potentially harmful content")

        if "description" in params:
            description = str(params["description"])
            if len(description) > 1000:
                warnings.append("Description is very long (max 1000 characters)")

            if not SafeContentValidator.validate_task_content(description):
                errors.append("Description contains potentially harmful content")

        return {
            "is_valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings
        }

    @staticmethod
    def validate_task_id(task_id: str) -> bool:
        """
        Validate task ID format
        """
        if not task_id:
            return False

        # Basic UUID format check
        uuid_pattern = r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
        return bool(re.match(uuid_pattern, task_id.lower()))

    @staticmethod
    def validate_update_task_params(params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate parameters for updating a task
        """
        errors = []
        warnings = []

        if "task_id" not in params or not params["task_id"]:
            errors.append("Task ID is required for update operation")

        if "task_id" in params and not TaskOperationValidator.validate_task_id(params["task_id"]):
            errors.append("Invalid task ID format")

        if "title" in params and params["title"]:
            title = str(params["title"])
            if len(title) > 200:
                errors.append("Title is too long (max 200 characters)")

            if not SafeContentValidator.validate_task_content(title):
                errors.append("Title contains potentially harmful content")

        if "description" in params and params["description"]:
            description = str(params["description"])
            if len(description) > 1000:
                warnings.append("Description is very long (max 1000 characters)")

            if not SafeContentValidator.validate_task_content(description):
                errors.append("Description contains potentially harmful content")

        return {
            "is_valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings
        }


class SecurityValidator:
    """
    Main security validation class
    """
    @staticmethod
    def validate_chat_request(message: str, conversation_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Validate a complete chat request
        """
        message_validation = ChatRequestValidator.validate_message(message)
        conversation_validation = ChatRequestValidator.validate_conversation_id(conversation_id)

        return {
            "message_valid": message_validation["is_valid"],
            "conversation_valid": conversation_validation["is_valid"],
            "all_valid": message_validation["is_valid"] and conversation_validation["is_valid"],
            "message_errors": message_validation["errors"],
            "conversation_errors": [] if conversation_validation["is_valid"] else ["Invalid conversation ID"],
            "sanitized_message": message_validation["sanitized_message"]
        }

    @staticmethod
    def validate_task_operation(operation_type: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate a task operation
        """
        if operation_type == "add_task":
            return TaskOperationValidator.validate_add_task_params(params)
        elif operation_type == "update_task":
            return TaskOperationValidator.validate_update_task_params(params)
        elif operation_type in ["complete_task", "delete_task"]:
            # For these operations, we mainly need to validate the task_id
            if "task_id" not in params or not params["task_id"]:
                return {
                    "is_valid": False,
                    "errors": ["Task ID is required"],
                    "warnings": []
                }

            if not TaskOperationValidator.validate_task_id(params["task_id"]):
                return {
                    "is_valid": False,
                    "errors": ["Invalid task ID format"],
                    "warnings": []
                }

            return {
                "is_valid": True,
                "errors": [],
                "warnings": []
            }
        else:
            return {
                "is_valid": True,
                "errors": [],
                "warnings": []
            }