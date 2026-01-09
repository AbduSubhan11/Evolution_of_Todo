from sqlmodel import Session, select
from typing import List, Optional
from uuid import UUID
from ..models.task import Task, TaskCreate, TaskUpdate


def create_task(*, session: Session, task_create: TaskCreate, user_id: UUID) -> Task:
    """
    Create a new task for a specific user
    """
    # Create the task object with the user_id
    db_task = Task(
        title=task_create.title,
        description=task_create.description,
        status=task_create.status,
        user_id=user_id
    )

    # Add to session and commit
    session.add(db_task)
    session.commit()
    session.refresh(db_task)

    return db_task


def get_tasks_by_user(*, session: Session, user_id: UUID, status: Optional[str] = None,
                      limit: Optional[int] = None, offset: Optional[int] = None) -> List[Task]:
    """
    Get all tasks for a specific user, with optional filtering
    """
    statement = select(Task).where(Task.user_id == user_id)

    if status:
        statement = statement.where(Task.status == status)

    if offset:
        statement = statement.offset(offset)

    if limit:
        statement = statement.limit(limit)

    tasks = session.exec(statement).all()
    return tasks


def get_task_by_id(*, session: Session, task_id: UUID, user_id: UUID) -> Optional[Task]:
    """
    Get a specific task by ID for a specific user
    """
    statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    task = session.exec(statement).first()
    return task


def update_task(*, session: Session, task_id: UUID, user_id: UUID, task_update: TaskUpdate) -> Optional[Task]:
    """
    Update a specific task for a specific user
    """
    db_task = session.get(Task, task_id)
    if not db_task or db_task.user_id != user_id:
        return None

    # Update the task with the provided fields
    update_data = task_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_task, field, value)

    session.add(db_task)
    session.commit()
    session.refresh(db_task)

    return db_task


def delete_task(*, session: Session, task_id: UUID, user_id: UUID) -> bool:
    """
    Delete a specific task for a specific user
    """
    db_task = session.get(Task, task_id)
    if not db_task or db_task.user_id != user_id:
        return False

    session.delete(db_task)
    session.commit()
    return True


def toggle_task_completion(*, session: Session, task_id: UUID, user_id: UUID, complete: bool) -> Optional[Task]:
    """
    Toggle completion status of a specific task for a specific user
    """
    db_task = session.get(Task, task_id)
    if not db_task or db_task.user_id != user_id:
        return None

    # Update completion status
    if complete:
        db_task.status = "completed"
        # Set completed_at to current time if not already set
        from datetime import datetime
        if not db_task.completed_at:
            db_task.completed_at = datetime.utcnow()
    else:
        db_task.status = "pending"
        # Clear completed_at if setting to pending
        db_task.completed_at = None

    session.add(db_task)
    session.commit()
    session.refresh(db_task)

    return db_task