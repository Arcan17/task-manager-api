from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.routers import tasks

app = FastAPI(
    title="Task Manager API",
    description="A RESTful API for managing tasks with full CRUD operations.",
    version="1.0.0",
)

app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(tasks.router)


@app.get("/", include_in_schema=False)
def index():
    return FileResponse("static/index.html")


@app.get("/health", tags=["health"])
def health_check():
    return {"status": "healthy"}
