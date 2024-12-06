from fastapi import FastAPI
from app.routes import tasks, auth, users
from app.config import engine
from app.models import user, task

# Create database tables
user.Base.metadata.create_all(bind=engine)
task.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Task Management API")

# Include routers
app.include_router(auth.router)
app.include_router(tasks.router)
app.include_router(users.router)
