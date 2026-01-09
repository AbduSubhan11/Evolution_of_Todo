from sqlmodel import Session, select
from typing import Optional
from ..models.user import User, UserCreate
from ..auth.security import get_password_hash


def create_user(*, session: Session, user_create: UserCreate) -> User:
    """
    Create a new user in the database
    """
    # Hash the password
    hashed_password = get_password_hash(user_create.password)

    # Create the user object
    db_user = User(
        email=user_create.email,
        password_hash=hashed_password
    )

    # Add to session and commit
    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


def get_user_by_email(*, session: Session, email: str) -> Optional[User]:
    """
    Get a user by email
    """
    statement = select(User).where(User.email == email)
    user = session.exec(statement).first()
    return user


def get_user_by_id(*, session: Session, user_id: str) -> Optional[User]:
    """
    Get a user by ID
    """
    statement = select(User).where(User.id == user_id)
    user = session.exec(statement).first()
    return user


def update_user(*, session: Session, user_id: str, user_update: dict) -> Optional[User]:
    """
    Update a user in the database
    """
    db_user = session.get(User, user_id)
    if not db_user:
        return None

    # Update the user with the provided fields
    for field, value in user_update.items():
        setattr(db_user, field, value)

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


def delete_user(*, session: Session, user_id: str) -> bool:
    """
    Delete a user from the database
    """
    db_user = session.get(User, user_id)
    if not db_user:
        return False

    session.delete(db_user)
    session.commit()
    return True