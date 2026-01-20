from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.v1.endpoints import tasks
from .api.v1.endpoints import chat
from .auth.routers import router as auth_router
from .database import engine
from .models import user, task  # Import models to register them
from .middleware.auth import jwt_auth_middleware
from .api.error_handlers import add_global_exception_handlers

# Create tables
user.SQLModel.metadata.create_all(bind=engine)
task.SQLModel.metadata.create_all(bind=engine)

app = FastAPI(title="Todo API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
        "http://localhost:3002",
        "http://localhost:3003",
        "http://localhost:3004",
        "http://localhost:3005",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001",
        "http://127.0.0.1:3002",
        "http://127.0.0.1:3003",
        "http://127.0.0.1:3004",
        "http://127.0.0.1:3005"
    ],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add JWT auth middleware
@app.middleware("http")
async def add_jwt_middleware(request, call_next):
    response = await jwt_auth_middleware(request, call_next)
    return response

# Include routers
app.include_router(auth_router, prefix="/api/auth", tags=["auth"])
app.include_router(tasks.router, prefix="/api", tags=["tasks"])
app.include_router(chat.router, prefix="/api/v1", tags=["chat"])

@app.get("/api/auth/health")
def auth_health():
    return {"status": "auth service healthy"}

@app.get("/")
def read_root():
    return {"message": "Todo API is running!"}



@app.get("/health")
def health_check():
    return {"status": "healthy"}

# Add global exception handlers
add_global_exception_handlers(app)