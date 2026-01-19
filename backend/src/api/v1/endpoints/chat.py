from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlmodel import Session
from uuid import UUID
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
import json

# Import with correct relative paths from src/api/v1/endpoints/chat.py
from ....database import get_session
from ....models.user import User
from ....utils.ai_client import ai_client, AIResponse

# For imports from the core directory, use sys.path manipulation
import sys
import os
backend_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))  # Go from src/api/v1/endpoints to backend root
sys.path.append(backend_root)

from core.agents.chat_agent import initialize_chat_agent
from core.tools.task_tools import execute_tool_call

router = APIRouter()

class ChatRequest(BaseModel):
    conversation_id: Optional[str] = None
    message: str

class ChatResponse(BaseModel):
    conversation_id: str
    response: str
    tool_calls: List[Dict[str, Any]]
    status: str

@router.post("/{user_id}/chat", response_model=ChatResponse)
async def chat(
    user_id: UUID,
    request: Request,
    chat_request: ChatRequest,
    session: Session = Depends(get_session)
):
    """
    Chat endpoint that allows users to interact with the AI assistant to manage tasks
    """
    # Verify the user_id matches the authenticated user
    authenticated_user_id = getattr(request.state, 'user_id', None)
    if authenticated_user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User not authorized to access this chat"
        )

    # Verify the user exists
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    try:
        # Initialize the chat agent with tools for this user
        assistant_id = await initialize_chat_agent(user_id)

        # If no conversation_id provided, create a new thread
        if not chat_request.conversation_id:
            thread_id = await ai_client.create_thread()
        else:
            thread_id = chat_request.conversation_id

        # Add the user's message to the thread
        await ai_client.add_message_to_thread(thread_id, chat_request.message)

        # Run the assistant and get response
        response, run_id = await ai_client.run_assistant(thread_id, assistant_id)

        # If there are tool calls in the response, execute them and submit results
        if response.tool_calls:
            # Execute each tool call and collect results
            tool_outputs = []
            for tool_call in response.tool_calls:
                function_name = tool_call.get("function", {}).get("name")
                arguments_str = tool_call.get("function", {}).get("arguments", "{}")

                try:
                    # Parse the arguments
                    arguments = json.loads(arguments_str) if arguments_str else {}

                    # Execute the tool
                    result = await execute_tool_call(str(user_id), function_name, arguments)

                    # Format the output for OpenAI
                    tool_outputs.append({
                        "tool_call_id": tool_call["id"],
                        "output": json.dumps(result)
                    })
                except Exception as e:
                    tool_outputs.append({
                        "tool_call_id": tool_call["id"],
                        "output": json.dumps({"error": str(e)})
                    })

            # Submit the tool outputs back to the assistant to get the final response
            if tool_outputs:
                final_response = await ai_client.submit_tool_outputs(thread_id, run_id, tool_outputs)
                # Update the response with the final response from the assistant
                response = final_response

        return ChatResponse(
            conversation_id=thread_id,
            response=response.content,
            tool_calls=getattr(response, 'tool_calls', []) or [],  # Handle case where response after tool execution might not have tool_calls
            status="success"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing chat request: {str(e)}"
        )