import openai
from typing import Dict, Any, List, Optional
import sys
import os
import json
import re
from dotenv import load_dotenv

# Add the backend root directory to the Python path
backend_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(backend_root)

from config.openai_config import ai_config
from pydantic import BaseModel
import logging

logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

class AIError(Exception):
    """Custom exception for AI-related errors"""
    pass

class AIResponse(BaseModel):
    """Model for AI responses"""
    content: str
    tool_calls: Optional[List[Dict[str, Any]]] = []
    conversation_id: Optional[str] = None

class AIClient:
    """
    Client for interacting with Google Gemini API through OpenAI SDK
    """

    def __init__(self):
        if not ai_config.api_key:
            raise AIError("GEMINI_API_KEY environment variable is not set. Please configure your API key.")

        # Initialize OpenAI client with Google's Gemini endpoint
        self.client = openai.AsyncOpenAI(
            api_key=ai_config.api_key,
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
        )

        # Use the model from configuration
        self.model = ai_config.model
        self.chat_history = []  # Store conversation history for context

    async def create_assistant(self, instructions: str, tools: List[Dict[str, Any]]) -> str:
        """
        Create an assistant with specific instructions and tools
        """
        try:
            # In this implementation, we'll return the instructions as the assistant ID
            # since we're simulating the assistant concept
            assistant_id = f"gemini-openai-{hash(instructions) % 10000}"
            return assistant_id
        except Exception as e:
            logger.error(f"Failed to create assistant: {str(e)}")
            raise AIError(f"Failed to create assistant: {str(e)}")

    async def create_thread(self) -> str:
        """
        Create a new conversation thread
        """
        try:
            import uuid
            thread_id = str(uuid.uuid4())
            # Initialize a new chat session for this thread
            self.chat_history = []
            return thread_id
        except Exception as e:
            logger.error(f"Failed to create thread: {str(e)}")
            raise AIError(f"Failed to create thread: {str(e)}")

    async def add_message_to_thread(self, thread_id: str, message: str) -> str:
        """
        Add a message to an existing thread
        """
        try:
            # Store the message in chat history
            self.chat_history.append({"role": "user", "content": message})
            return f"message-{thread_id[:8]}"
        except Exception as e:
            logger.error(f"Failed to add message to thread: {str(e)}")
            raise AIError(f"Failed to add message to thread: {str(e)}")

    async def run_assistant(self, thread_id: str, assistant_id: str) -> tuple[AIResponse, str]:
        """
        Run the assistant on a thread and get response with proper function calling
        """
        try:
            # Prepare messages for the API call
            messages = self.chat_history[:]

            # Get the latest user message
            latest_message = self.chat_history[-1]["content"] if self.chat_history else "Hello"

            # Check if it's a greeting message to provide appropriate response
            greeting_patterns = [
                r'hi|hello|hey|greetings|good morning|good afternoon|good evening',
                r'what.*up|how.*doing|how.*going|how.*are you',
                r'help|assist|support'
            ]

            is_greeting = any(re.search(pattern, latest_message.lower()) for pattern in greeting_patterns)

            # If it's a greeting, ensure proper response
            if is_greeting:
                messages[-1]["content"] = "Hello, how can I help you today?"

            # Call the OpenAI-compatible API with tools
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=[
                    {
                        "type": "function",
                        "function": {
                            "name": "add_task",
                            "description": "Add a new task",
                            "parameters": {
                                "type": "object",
                                "properties": {
                                    "title": {"type": "string", "description": "The title of the task"},
                                    "description": {"type": "string", "description": "The description of the task"}
                                },
                                "required": ["title"]
                            }
                        }
                    },
                    {
                        "type": "function",
                        "function": {
                            "name": "list_tasks",
                            "description": "List existing tasks with optional filtering",
                            "parameters": {
                                "type": "object",
                                "properties": {
                                    "status_filter": {
                                        "type": "string",
                                        "enum": ["pending", "completed", "archived"],
                                        "description": "Filter tasks by status"
                                    }
                                }
                            }
                        }
                    },
                    {
                        "type": "function",
                        "function": {
                            "name": "complete_task",
                            "description": "Mark a task as completed",
                            "parameters": {
                                "type": "object",
                                "properties": {
                                    "task_id": {"type": "string", "description": "The ID of the task to complete"},
                                    "title": {"type": "string", "description": "The title of the task to complete (partial match allowed)"}
                                }
                            }
                        }
                    },
                    {
                        "type": "function",
                        "function": {
                            "name": "uncomplete_task",
                            "description": "Mark a task as pending/uncompleted",
                            "parameters": {
                                "type": "object",
                                "properties": {
                                    "task_id": {"type": "string", "description": "The ID of the task to uncomplete"},
                                    "title": {"type": "string", "description": "The title of the task to uncomplete (partial match allowed)"}
                                }
                            }
                        }
                    },
                    {
                        "type": "function",
                        "function": {
                            "name": "delete_task",
                            "description": "Delete a task",
                            "parameters": {
                                "type": "object",
                                "properties": {
                                    "task_id": {"type": "string", "description": "The ID of the task to delete"},
                                    "title": {"type": "string", "description": "The title of the task to delete (partial match allowed)"}
                                }
                            }
                        }
                    },
                    {
                        "type": "function",
                        "function": {
                            "name": "update_task",
                            "description": "Update a task's details",
                            "parameters": {
                                "type": "object",
                                "properties": {
                                    "task_id": {"type": "string", "description": "The ID of the task to update"},
                                    "existing_title": {"type": "string", "description": "The current title of the task to update (partial match allowed)"},
                                    "title": {"type": "string", "description": "The new title for the task"},
                                    "description": {"type": "string", "description": "The new description for the task"},
                                    "status": {
                                        "type": "string",
                                        "enum": ["pending", "completed", "archived"],
                                        "description": "The new status for the task"
                                    }
                                }
                            }
                        }
                    }
                ],
                tool_choice="auto"  # Allow the model to decide when to use tools
            )

            # Extract the response
            choice = response.choices[0]
            message = choice.message

            content = message.content or ""

            # Process tool calls if any
            tool_calls = []
            if message.tool_calls:
                for tool_call in message.tool_calls:
                    tool_calls.append({
                        "id": tool_call.id,
                        "function": {
                            "name": tool_call.function.name,
                            "arguments": tool_call.function.arguments
                        },
                        "type": "function"
                    })

            # Update chat history with the AI response
            self.chat_history.append({"role": "assistant", "content": content})

            ai_response = AIResponse(
                content=content,
                tool_calls=tool_calls
            )

            # Return the response and a run_id
            return ai_response, f"run-{thread_id[:8]}"
        except Exception as e:
            logger.error(f"Failed to run assistant: {str(e)}")
            raise AIError(f"Failed to run assistant: {str(e)}")

    async def submit_tool_outputs(self, thread_id: str, run_id: str, tool_outputs: List[Dict[str, Any]]) -> AIResponse:
        """
        Submit tool outputs to continue the run and get the final response
        """
        try:
            # Process the tool outputs to get results
            tool_output_results = []
            for output in tool_outputs:
                output_data = output.get("output", "{}")
                try:
                    parsed_output = json.loads(output_data)
                    tool_output_results.append(parsed_output)
                except json.JSONDecodeError:
                    tool_output_results.append({"raw_output": output_data})

            # Format a clear response based on tool execution results
            success_messages = []
            error_messages = []

            for result in tool_output_results:
                if isinstance(result, dict):
                    if result.get("success"):
                        success_msg = result.get("message", "Operation completed successfully")
                        success_messages.append(success_msg)
                    else:
                        error_msg = result.get("message", "Operation failed")
                        error_messages.append(error_msg)

            if success_messages:
                final_content = " ".join(success_messages)
            elif error_messages:
                final_content = "Error: " + " ".join(error_messages)
            else:
                final_content = "Operation completed."

            # Update chat history with the final response
            self.chat_history.append({"role": "assistant", "content": final_content})

            return AIResponse(content=final_content)
        except Exception as e:
            logger.error(f"Failed to submit tool outputs: {str(e)}")
            raise AIError(f"Failed to submit tool outputs: {str(e)}")

# Global instance
ai_client = AIClient()