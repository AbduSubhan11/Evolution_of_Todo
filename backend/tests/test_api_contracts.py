import pytest
from fastapi.testclient import TestClient
from fastapi.openapi.utils import validate_openapi_path
from fastapi import FastAPI
from uuid import uuid4
import json
import sys
import os

# Add the src directory to the path so we can import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from main import app  # Adjust import based on your main app location

client = TestClient(app)


def test_openapi_schema_exists():
    """Test that the OpenAPI schema is available"""
    response = client.get("/openapi.json")
    assert response.status_code == 200

    schema = response.json()
    assert "openapi" in schema
    assert "paths" in schema
    assert schema["openapi"].startswith("3.")


def test_chat_endpoint_in_openapi():
    """Test that the chat endpoint is documented in OpenAPI schema"""
    response = client.get("/openapi.json")
    assert response.status_code == 200

    schema = response.json()

    # Check that the chat endpoint exists in the schema
    paths = schema["paths"]
    # The chat endpoint should be available with a parameterized path
    chat_paths = [path for path in paths.keys() if "chat" in path.lower()]
    assert len(chat_paths) >= 1  # Should have at least one chat-related path


def test_chat_endpoint_method_and_parameters():
    """Test that the chat endpoint has the correct method and parameters"""
    response = client.get("/openapi.json")
    assert response.status_code == 200

    schema = response.json()

    # Find the chat endpoint
    chat_path = None
    for path, methods in schema["paths"].items():
        if "/chat" in path and "post" in methods:
            chat_path = path
            break

    assert chat_path is not None, "Chat endpoint not found in OpenAPI schema"

    # Get the POST method definition for the chat endpoint
    post_definition = schema["paths"][chat_path]["post"]

    # Verify the endpoint has the correct method
    assert "post" in schema["paths"][chat_path]

    # Verify the endpoint has a request body defined
    assert "requestBody" in post_definition
    request_body = post_definition["requestBody"]

    # Verify the request body has content
    assert "content" in request_body
    content_types = list(request_body["content"].keys())
    assert "application/json" in content_types

    # Verify the request body schema
    json_schema = request_body["content"]["application/json"]["schema"]
    assert "properties" in json_schema
    properties = json_schema["properties"]

    # Verify required properties
    if "required" in json_schema:
        required_fields = json_schema["required"]
        # At minimum, we should require the message field
        assert "message" in required_fields or any("message" in prop.lower() for prop in required_fields)


@pytest.mark.parametrize("param_value", [
    str(uuid4()),
    "123e4567-e89b-12d3-a456-426614174000",
    "valid-user-id-123"
])
def test_chat_endpoint_accepts_valid_user_ids(param_value):
    """Test that the chat endpoint accepts various valid user ID formats"""
    # This test verifies that the path parameter accepts valid formats
    response = client.post(
        f"/api/{param_value}/chat",
        json={
            "message": "test"
        },
        headers={
            "Authorization": "Bearer test-token"
        }
    )

    # We expect either a 422 (validation error due to missing token/invalid auth)
    # or 401/403 (unauthorized) or 200 (success) depending on auth setup
    # But it shouldn't return 404 (endpoint not found)
    assert response.status_code != 404


def test_chat_endpoint_request_body_schema():
    """Test that the chat endpoint has the correct request body schema"""
    response = client.get("/openapi.json")
    assert response.status_code == 200

    schema = response.json()

    # Find the chat endpoint
    chat_path = None
    for path, methods in schema["paths"].items():
        if "/chat" in path and "post" in methods:
            chat_path = path
            break

    assert chat_path is not None

    post_definition = schema["paths"][chat_path]["post"]
    request_body = post_definition["requestBody"]["content"]["application/json"]["schema"]

    # Verify the properties structure
    assert "properties" in request_body
    props = request_body["properties"]

    # The message property should exist
    assert "message" in props or any("message" in prop for prop in props)


def test_chat_endpoint_response_schema():
    """Test that the chat endpoint has the correct response schema"""
    response = client.get("/openapi.json")
    assert response.status_code == 200

    schema = response.json()

    # Find the chat endpoint
    chat_path = None
    for path, methods in schema["paths"].items():
        if "/chat" in path and "post" in methods:
            chat_path = path
            break

    assert chat_path is not None

    post_definition = schema["paths"][chat_path]["post"]

    # Verify responses are defined
    assert "responses" in post_definition
    responses = post_definition["responses"]

    # Should have at least a 200 response
    assert "200" in responses or "default" in responses

    # Check the response schema
    success_response = responses.get("200", responses.get("default"))
    if success_response and "content" in success_response:
        content = success_response["content"]
        if "application/json" in content:
            response_schema = content["application/json"]["schema"]

            # The response should have expected properties
            if "properties" in response_schema:
                response_props = response_schema["properties"]
                # Should have conversation_id, response, and status at minimum
                expected_props = {"conversation_id", "response", "status"}
                actual_props = set(response_props.keys())

                # Check that we have at least the essential response properties
                assert len(actual_props.intersection(expected_props)) >= 2


def test_api_contract_compliance_basic():
    """Basic compliance test for API contract adherence"""
    # Get the OpenAPI schema
    schema_response = client.get("/openapi.json")
    assert schema_response.status_code == 200
    schema = schema_response.json()

    # Verify basic OpenAPI structure
    assert "openapi" in schema
    assert "info" in schema
    assert "paths" in schema

    # Verify that the schema version is valid
    assert schema["openapi"].startswith("3.")

    # Count chat-related endpoints
    chat_endpoints = []
    for path, methods in schema["paths"].items():
        if "chat" in path.lower():
            chat_endpoints.append(path)

    # Should have at least one chat endpoint
    assert len(chat_endpoints) >= 1, f"No chat endpoints found in schema. Paths: {list(schema['paths'].keys())}"