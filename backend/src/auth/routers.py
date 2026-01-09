from fastapi import APIRouter, Depends, HTTPException, status, Form
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session, select
from typing import Optional
from datetime import timedelta
from ..database import get_session
from ..models.user import User, UserCreate, UserRead
from .security import verify_password, get_password_hash, create_access_token
from ..config import ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
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

    return {
        "id": db_user.id,
        "email": db_user.email,
        "created_at": db_user.created_at,
        "updated_at": db_user.updated_at,
        "token": access_token
    }

@router.post("/login")
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

    return {
        "user": {
            "id": user.id,
            "email": user.email,
        },
        "token": access_token
    }

@router.post("/logout")
def logout():
    """Invalidate user session."""
    # In a real implementation, you might add the token to a blacklist
    return {"message": "Successfully logged out"}