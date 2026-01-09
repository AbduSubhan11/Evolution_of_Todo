#!/usr/bin/env python3
"""
Test script to verify authentication and task CRUD operations
"""
import requests
import uuid
import time
import subprocess
import signal
import os
from threading import Thread
import sys

# Add the src directory to the path so we can import the modules directly
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_server():
    """Test the authentication and task endpoints"""
    base_url = "http://127.0.0.1:8001"

    print("Testing server endpoints...")

    # Test health endpoint
    try:
        response = requests.get(f"{base_url}/health")
        print(f"Health check: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"Health check failed: {e}")
        return False

    # Test auth health endpoint
    try:
        response = requests.get(f"{base_url}/api/auth/health")
        print(f"Auth health check: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"Auth health check failed: {e}")
        return False

    # Test registration
    test_email = f"testuser_{uuid.uuid4()}@example.com"
    test_password = "password123"

    try:
        response = requests.post(f"{base_url}/api/auth/register", json={
            "email": test_email,
            "password": test_password
        })
        print(f"Registration: {response.status_code}")
        if response.status_code == 201:
            user_data = response.json()
            print(f"User created: {user_data.get('id')}")
            token = user_data.get('token', '')
        else:
            print(f"Registration failed: {response.text}")
            return False
    except Exception as e:
        print(f"Registration failed with exception: {e}")
        return False

    # Test login
    try:
        response = requests.post(f"{base_url}/api/auth/login", data={
            "email": test_email,
            "password": test_password
        })
        print(f"Login: {response.status_code}")
        if response.status_code == 200:
            login_data = response.json()
            token = login_data.get('token', '')
            user_id = login_data.get('user', {}).get('id', '')
            print(f"Login successful, token: {token[:20]}...")
        else:
            print(f"Login failed: {response.text}")
            return False
    except Exception as e:
        print(f"Login failed with exception: {e}")
        return False

    # Test task operations with the token
    headers = {"Authorization": f"Bearer {token}"}

    # Test getting tasks (should be empty initially)
    try:
        response = requests.get(f"{base_url}/api/{user_id}/tasks", headers=headers)
        print(f"Get tasks: {response.status_code}")
        if response.status_code == 200:
            tasks = response.json()
            print(f"Tasks retrieved: {len(tasks)} tasks")
        else:
            print(f"Get tasks failed: {response.text}")
            return False
    except Exception as e:
        print(f"Get tasks failed with exception: {e}")
        return False

    # Test creating a task
    try:
        response = requests.post(f"{base_url}/api/{user_id}/tasks", json={
            "title": "Test task",
            "description": "This is a test task"
        }, headers=headers)
        print(f"Create task: {response.status_code}")
        if response.status_code == 201:
            task = response.json()
            task_id = task.get('id')
            print(f"Task created: {task_id}")
        else:
            print(f"Create task failed: {response.text}")
            return False
    except Exception as e:
        print(f"Create task failed with exception: {e}")
        return False

    # Test getting the specific task
    try:
        response = requests.get(f"{base_url}/api/{user_id}/tasks/{task_id}", headers=headers)
        print(f"Get specific task: {response.status_code}")
        if response.status_code == 200:
            task = response.json()
            print(f"Task retrieved: {task.get('title')}")
        else:
            print(f"Get specific task failed: {response.text}")
            return False
    except Exception as e:
        print(f"Get specific task failed with exception: {e}")
        return False

    # Test updating the task
    try:
        response = requests.put(f"{base_url}/api/{user_id}/tasks/{task_id}", json={
            "title": "Updated test task",
            "description": "This is an updated test task"
        }, headers=headers)
        print(f"Update task: {response.status_code}")
        if response.status_code == 200:
            task = response.json()
            print(f"Task updated: {task.get('title')}")
        else:
            print(f"Update task failed: {response.text}")
            return False
    except Exception as e:
        print(f"Update task failed with exception: {e}")
        return False

    # Test deleting the task
    try:
        response = requests.delete(f"{base_url}/api/{user_id}/tasks/{task_id}", headers=headers)
        print(f"Delete task: {response.status_code}")
        if response.status_code == 200:
            print("Task deleted successfully")
        else:
            print(f"Delete task failed: {response.text}")
            return False
    except Exception as e:
        print(f"Delete task failed with exception: {e}")
        return False

    print("All tests passed successfully!")
    return True

if __name__ == "__main__":
    print("Starting authentication and task CRUD tests...")
    success = test_server()
    if success:
        print("All tests completed successfully!")
    else:
        print("Some tests failed!")
        exit(1)