import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base, get_db
from app.main import app

TEST_DATABASE_URL = "sqlite:///./test_db.db"

engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def client():
    Base.metadata.create_all(bind=engine)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as c:
        yield c

    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=engine)


# ── Create ────────────────────────────────────────────────────────────────────


def test_create_task_minimal(client):
    response = client.post("/tasks/", json={"title": "Buy groceries"})
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Buy groceries"
    assert data["status"] == "pending"
    assert data["description"] is None
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data


def test_create_task_all_fields(client):
    payload = {
        "title": "Deploy app",
        "description": "Deploy to prod",
        "status": "in_progress",
    }
    response = client.post("/tasks/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Deploy app"
    assert data["description"] == "Deploy to prod"
    assert data["status"] == "in_progress"


def test_create_task_empty_title_fails(client):
    assert client.post("/tasks/", json={"title": ""}).status_code == 422


def test_create_task_missing_title_fails(client):
    assert client.post("/tasks/", json={"description": "No title"}).status_code == 422


def test_create_task_invalid_status_fails(client):
    assert (
        client.post("/tasks/", json={"title": "X", "status": "invalid"}).status_code
        == 422
    )


# ── List ──────────────────────────────────────────────────────────────────────


def test_list_tasks_empty(client):
    response = client.get("/tasks/")
    assert response.status_code == 200
    data = response.json()
    assert data["tasks"] == []
    assert data["total"] == 0


def test_list_tasks(client):
    client.post("/tasks/", json={"title": "Task 1"})
    client.post("/tasks/", json={"title": "Task 2"})
    response = client.get("/tasks/")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 2
    assert len(data["tasks"]) == 2


def test_list_tasks_filter_by_status(client):
    client.post("/tasks/", json={"title": "Pending task", "status": "pending"})
    client.post("/tasks/", json={"title": "Done task", "status": "done"})
    client.post("/tasks/", json={"title": "In progress", "status": "in_progress"})

    response = client.get("/tasks/?status=pending")
    data = response.json()
    assert data["total"] == 1
    assert data["tasks"][0]["title"] == "Pending task"

    response = client.get("/tasks/?status=done")
    data = response.json()
    assert data["total"] == 1
    assert data["tasks"][0]["title"] == "Done task"


def test_list_tasks_pagination(client):
    for i in range(5):
        client.post("/tasks/", json={"title": f"Task {i}"})

    response = client.get("/tasks/?skip=0&limit=2")
    data = response.json()
    assert len(data["tasks"]) == 2
    assert data["total"] == 5

    response = client.get("/tasks/?skip=2&limit=2")
    assert len(response.json()["tasks"]) == 2


# ── Get ───────────────────────────────────────────────────────────────────────


def test_get_task(client):
    task_id = client.post("/tasks/", json={"title": "Find me"}).json()["id"]
    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json()["title"] == "Find me"


def test_get_task_not_found(client):
    response = client.get("/tasks/9999")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


# ── Update ────────────────────────────────────────────────────────────────────


def test_update_task_title(client):
    task_id = client.post("/tasks/", json={"title": "Original"}).json()["id"]
    response = client.patch(f"/tasks/{task_id}", json={"title": "Updated"})
    assert response.status_code == 200
    assert response.json()["title"] == "Updated"


def test_update_task_status(client):
    task_id = client.post("/tasks/", json={"title": "My task"}).json()["id"]
    response = client.patch(f"/tasks/{task_id}", json={"status": "done"})
    assert response.status_code == 200
    assert response.json()["status"] == "done"


def test_update_task_partial_fields_preserved(client):
    task_id = client.post(
        "/tasks/", json={"title": "My task", "description": "Original desc"}
    ).json()["id"]
    response = client.patch(f"/tasks/{task_id}", json={"status": "in_progress"})
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "in_progress"
    assert data["title"] == "My task"
    assert data["description"] == "Original desc"


def test_update_task_not_found(client):
    assert client.patch("/tasks/9999", json={"title": "Nope"}).status_code == 404


def test_update_task_invalid_status(client):
    task_id = client.post("/tasks/", json={"title": "My task"}).json()["id"]
    assert (
        client.patch(f"/tasks/{task_id}", json={"status": "invalid"}).status_code == 422
    )


# ── Delete ────────────────────────────────────────────────────────────────────


def test_delete_task(client):
    task_id = client.post("/tasks/", json={"title": "Delete me"}).json()["id"]
    assert client.delete(f"/tasks/{task_id}").status_code == 204
    assert client.get(f"/tasks/{task_id}").status_code == 404


def test_delete_task_not_found(client):
    assert client.delete("/tasks/9999").status_code == 404


# ── Health ────────────────────────────────────────────────────────────────────


def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}
