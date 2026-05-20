"""
Team Task Manager — FastAPI application entry point.
"""

import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import get_engine, Base
from app.routes import auth_routes, project_routes, task_routes, dashboard_routes

load_dotenv()

app = FastAPI(
    title="Team Task Manager API",
    description="Beginner-friendly task management API with JWT auth",
    version="1.0.0",
)

# CORS — allow frontend (Netlify, Vercel, or local static server)
origins = os.getenv("CORS_ORIGINS", "http://127.0.0.1:5500")
allow_origins = [o.strip() for o in origins.split(",") if o.strip()]
# Common local URLs (python http.server may open as 0.0.0.0 or localhost)
for origin in (
    "http://127.0.0.1:5500",
    "http://localhost:5500",
    "http://0.0.0.0:5500",
):
    if origin not in allow_origins:
        allow_origins.append(origin)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def create_tables():
    """Create database tables on first run (beginner-friendly)."""
    Base.metadata.create_all(bind=get_engine())


# Register route modules
app.include_router(auth_routes.router)
app.include_router(project_routes.router)
app.include_router(task_routes.router)
app.include_router(dashboard_routes.router)


@app.get("/")
def root():
    """Health check endpoint."""
    return {"message": "Team Task Manager API is running"}


@app.get("/health")
def health():
    return {"status": "ok"}
