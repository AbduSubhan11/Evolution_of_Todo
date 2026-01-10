from fastapi import APIRouter, Depends, HTTPException, status, Form
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session, select
from typing import Optional
from datetime import timedelta, datetime
import uuid
from ..database import get_session
from ..models.user import User, UserCreate, UserRead
from .security import verify_password, get_password_hash, create_access_token
from ..config import ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

from pydantic import BaseModel

class RegisterResponse(BaseModel):
    user: UserRead
    token: str

@router.post("/register", response_model=RegisterResponse, status_code=status.HTTP_201_CREATED)
def register(user_create: UserCreate, session: Session = Depends(get_session)):
    """Register a new user account."""
    # Check if user already exists
    existing_user = session.exec(select(User).where(User.email == user_create.email)).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )

    # Create new user
    hashed_password = get_password_hash(user_create.password)
    db_user = User(
        email=user_create.email,
        password_hash=hashed_password
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(db_user.id)}, expires_delta=access_token_expires
    )

    user_data = UserRead(
        id=db_user.id,
        email=db_user.email,
        created_at=db_user.created_at,
        updated_at=db_user.updated_at
    )

    return {
        "user": user_data,
        "token": access_token
    }

class LoginResponse(BaseModel):
    user: UserRead
    token: str

@router.post("/login", response_model=LoginResponse)
def login(email: str = Form(...), password: str = Form(...), session: Session = Depends(get_session)):
    """Authenticate user and return JWT token."""
    # Find user by email
    user = session.exec(select(User).where(User.email == email)).first()
    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )

    user_data = UserRead(
        id=user.id,
        email=user.email,
        created_at=user.created_at,
        updated_at=user.updated_at
    )

    return {
        "user": user_data,
        "token": access_token
    }

@router.post("/logout")
def logout():
    """Invalidate user session."""
    # In a real implementation, you might add the token to a blacklist
    return {"message": "Successfully logged out"}

@router.get("/session", response_model=UserRead)
def get_session(token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)):
    """Get current user session based on token."""
    from .security import verify_token, get_current_user_id

    payload = verify_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_id = payload.get("sub")
    try:
        user_uuid = uuid.UUID(user_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = session.get(User, user_uuid)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return UserRead(
        id=user.id,
        email=user.email,
        created_at=user.created_at,
        updated_at=user.updated_at
    )