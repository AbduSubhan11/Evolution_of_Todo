from fastapi import APIRouter, Depends, HTTPException, status, Query, Request
from sqlmodel import Session, select
from typing import List, Optional
from uuid import UUID
from datetime import datetime
from ....database import get_session
from ....models.task import Task, TaskCreate, TaskRead, TaskUpdate
from ....models.user import User

router = APIRouter()

@router.get("/{user_id}/tasks", response_model=List[TaskRead])
def get_tasks(
    user_id: UUID,
    request: Request,  # Access to request state set by middleware
    status_filter: Optional[str] = Query(None, description="Filter by status (pending, completed, archived)"),
    limit: Optional[int] = Query(None, ge=1, le=100, description="Number of results to return"),
    offset: Optional[int] = Query(None, ge=0, description="Number of results to skip"),
    session: Session = Depends(get_session)
):
    """
    Get all tasks for the authenticated user
    """
    # Verify the user_id matches the authenticated user
    authenticated_user_id = getattr(request.state, 'user_id', None)
    if authenticated_user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User not authorized to access these tasks"
        )

    # Build query
    query = select(Task).where(Task.user_id == user_id)

    if status_filter:
        query = query.where(Task.status == status_filter)

    if limit:
        query = query.limit(limit)

    if offset:
        query = query.offset(offset)

    tasks = session.exec(query).all()

    return tasks


@router.post("/{user_id}/tasks", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
def create_task(
    user_id: UUID,
    request: Request,
    task_create: TaskCreate,
    session: Session = Depends(get_session)
):
    """
    Create a new task for the authenticated user
    """
    # Verify the user_id matches the authenticated user
    authenticated_user_id = getattr(request.state, 'user_id', None)
    if authenticated_user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User not authorized to create tasks for this account"
        )

    # Verify the user exists
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Create the task with user_id
    task_data = task_create.model_dump()
    task_data['user_id'] = user_id
    db_task = Task(**task_data)

    session.add(db_task)
    session.commit()
    session.refresh(db_task)

    return db_task


@router.get("/{user_id}/tasks/{id}", response_model=TaskRead)
def get_task(
    user_id: UUID,
    id: UUID,
    request: Request,
    session: Session = Depends(get_session)
):
    """
    Get a specific task for the authenticated user
    """
    # Verify the user_id matches the authenticated user
    authenticated_user_id = getattr(request.state, 'user_id', None)
    if authenticated_user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User not authorized to access this task"
        )

    # Get the task
    task = session.get(Task, id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Verify that the task belongs to the user
    if task.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User not authorized to access this task"
        )

    return task


@router.put("/{user_id}/tasks/{id}", response_model=TaskRead)
def update_task(
    user_id: UUID,
    id: UUID,
    request: Request,
    task_update: TaskUpdate,
    session: Session = Depends(get_session)
):
    """
    Update a specific task for the authenticated user
    """
    # Verify the user_id matches the authenticated user
    authenticated_user_id = getattr(request.state, 'user_id', None)
    if authenticated_user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User not authorized to update this task"
        )

    # Get the existing task
    db_task = session.get(Task, id)
    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Verify that the task belongs to the user
    if db_task.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User not authorized to update this task"
        )

    # Update the task
    update_data = task_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_task, field, value)

    session.add(db_task)
    session.commit()
    session.refresh(db_task)

    return db_task


@router.delete("/{user_id}/tasks/{id}")
def delete_task(
    user_id: UUID,
    id: UUID,
    request: Request,
    session: Session = Depends(get_session)
):
    """
    Delete a specific task for the authenticated user
    """
    # Verify the user_id matches the authenticated user
    authenticated_user_id = getattr(request.state, 'user_id', None)
    if authenticated_user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User not authorized to delete this task"
        )

    # Get the existing task
    db_task = session.get(Task, id)
    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Verify that the task belongs to the user
    if db_task.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User not authorized to delete this task"
        )

    # Delete the task
    session.delete(db_task)
    session.commit()

    return {"message": "Task deleted successfully"}


from pydantic import BaseModel

class ToggleCompletionRequest(BaseModel):
    complete: bool

@router.patch("/{user_id}/tasks/{id}/complete")
def toggle_task_completion(
    user_id: UUID,
    id: UUID,
    request: Request,
    toggle_request: ToggleCompletionRequest,
    session: Session = Depends(get_session)
):
    """
    Toggle completion status of a task
    """
    # Verify the user_id matches the authenticated user
    authenticated_user_id = getattr(request.state, 'user_id', None)
    if authenticated_user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User not authorized to modify this task"
        )

    # Get the existing task
    db_task = session.get(Task, id)
    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Verify that the task belongs to the user
    if db_task.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User not authorized to modify this task"
        )

    # Update completion status
    if toggle_request.complete:
        db_task.status = "completed"
        db_task.completed_at = datetime.utcnow()
    else:
        db_task.status = "pending"
        db_task.completed_at = None

    session.add(db_task)
    session.commit()
    session.refresh(db_task)

    return {
        "id": db_task.id,
        "title": db_task.title,
        "status": db_task.status,
        "completed_at": db_task.completed_at
    }