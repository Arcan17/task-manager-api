# Task Manager API

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111-009688?style=flat&logo=fastapi&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-4169E1?style=flat&logo=postgresql&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-D71F00?style=flat)
![Docker](https://img.shields.io/badge/Docker-ready-2496ED?style=flat&logo=docker&logoColor=white)
![CI](https://img.shields.io/github/actions/workflow/status/Arcan17/task-manager-api/ci.yml?label=CI&logo=github)
![License](https://img.shields.io/badge/license-MIT-green?style=flat)
![Status](https://img.shields.io/badge/status-active-brightgreen)

A **production-ready RESTful API** for task management, built to demonstrate clean backend architecture with FastAPI, PostgreSQL, and SQLAlchemy. Includes full CRUD, status filtering, pagination, Alembic migrations, Docker Compose setup, 20+ automated tests, and GitHub Actions CI.

**Why this project:** Task managers are a familiar domain, which makes this ideal for demonstrating backend fundamentals clearly — without domain complexity getting in the way. The focus is on the architecture: proper ORM usage, schema validation, migration workflow, containerization, and test coverage.

---

## Client Use Case

This project is useful for clients who need to:
- **A clean REST API backend** for any web or mobile app
- **CRUD operations** with proper validation, error handling, and HTTP status codes
- **Filtered and paginated data** — query by status, date, priority, or any field
- **Production-ready architecture** — Docker, migrations, tests, CI/CD included
- **A starting point** for a task manager, project tracker, CRM, or any resource management system
- **API documentation** auto-generated (Swagger UI at `/docs`)

> Easily extended with: JWT authentication, user roles, WebSocket updates, email notifications, or any domain-specific fields.

---

## Live API Docs

Once running, interactive documentation is auto-generated at:
- **Swagger UI:** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`

| Swagger UI |
|---|
| ![Swagger UI](docs/screenshots/swagger-ui.png) |

---

## Features

- **Full CRUD** — create, list, retrieve, update, and delete tasks
- **Status filtering** — query tasks by `pending`, `in_progress`, or `done`
- **Pagination** — `skip` / `limit` query parameters on the list endpoint
- **Strict validation** — Pydantic v2 with descriptive error messages
- **Database migrations** — Alembic for version-controlled schema changes
- **Containerized** — single `docker-compose up` spins up the app and PostgreSQL
- **Automated tests** — 20+ pytest cases using an isolated SQLite database
- **CI/CD** — GitHub Actions runs the full test suite on every push to `main`
- **Interactive docs** — Swagger UI at `/docs`, ReDoc at `/redoc`

---

## Tech Stack

| Layer | Technology |
|---|---|
| Framework | FastAPI |
| Database | PostgreSQL 15 |
| ORM | SQLAlchemy 2.0 |
| Migrations | Alembic |
| Validation | Pydantic v2 |
| Testing | pytest + httpx |
| Containerization | Docker + Docker Compose |
| CI/CD | GitHub Actions |

---

## Project Structure

```
task-manager-api/
├── app/
│   ├── main.py          # FastAPI app and router registration
│   ├── database.py      # SQLAlchemy engine, session factory, Base
│   ├── models.py        # ORM models (Task, TaskStatus enum)
│   ├── schemas.py       # Pydantic schemas for request/response
│   └── routers/
│       └── tasks.py     # CRUD endpoints
├── tests/
│   └── test_tasks.py    # Full test suite (SQLite in-memory)
├── alembic/             # Migration scripts
│   └── versions/
│       └── 001_create_tasks_table.py
├── .github/
│   └── workflows/
│       └── ci.yml       # GitHub Actions CI
├── Dockerfile
├── docker-compose.yml
├── alembic.ini
├── requirements.txt
└── .env.example
```

---

## Getting Started

### Option 1: Docker (recommended)

**Prerequisites:** Docker and Docker Compose installed.

```bash
git clone https://github.com/Arcan17/task-manager-api.git
cd task-manager-api

docker-compose up --build
```

The API will be available at `http://localhost:8000`. Docker Compose will automatically:
1. Start a PostgreSQL 15 container
2. Run Alembic migrations
3. Launch the FastAPI application

### Option 2: Local Development

**Prerequisites:** Python 3.11+, PostgreSQL running locally.

```bash
git clone https://github.com/Arcan17/task-manager-api.git
cd task-manager-api

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your local PostgreSQL credentials

# Run database migrations
alembic upgrade head

# Start the server
uvicorn app.main:app --reload
```

---

## Running Tests

Tests use an isolated SQLite database — no running PostgreSQL required.

```bash
pytest tests/ -v
```

Expected output:

```
tests/test_tasks.py::test_create_task_minimal PASSED
tests/test_tasks.py::test_create_task_all_fields PASSED
tests/test_tasks.py::test_create_task_empty_title_fails PASSED
...
20 passed in 1.23s
```

---

## API Reference

### Base URL

```
http://localhost:8000
```

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/tasks/` | Create a new task |
| `GET` | `/tasks/` | List all tasks (supports filtering & pagination) |
| `GET` | `/tasks/{id}` | Get a single task |
| `PATCH` | `/tasks/{id}` | Partially update a task |
| `DELETE` | `/tasks/{id}` | Delete a task |
| `GET` | `/health` | Health check |

### Task Schema

```json
{
  "id": 1,
  "title": "Deploy application",
  "description": "Deploy the new release to production",
  "status": "in_progress",
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T11:00:00Z"
}
```

**Status values:** `pending` · `in_progress` · `done`

---

### Examples

**Create a task**
```bash
curl -X POST http://localhost:8000/tasks/ \
  -H "Content-Type: application/json" \
  -d '{"title": "Write tests", "description": "Add unit tests", "status": "pending"}'
```

**List all tasks**
```bash
curl http://localhost:8000/tasks/
```

**Filter by status**
```bash
curl "http://localhost:8000/tasks/?status=pending"
```

**Paginate results**
```bash
curl "http://localhost:8000/tasks/?skip=0&limit=10"
```

**Update a task**
```bash
curl -X PATCH http://localhost:8000/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{"status": "done"}'
```

**Delete a task**
```bash
curl -X DELETE http://localhost:8000/tasks/1
```

---

## Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://user:pass@localhost:5432/taskmanager` |
| `SECRET_KEY` | Secret key (reserved for future auth) | `your-random-secret-key` |

Copy `.env.example` to `.env` and fill in your values. Never commit `.env` to version control.

---

## Database Migrations

```bash
# Apply all pending migrations
alembic upgrade head

# Create a new migration after model changes
alembic revision --autogenerate -m "describe your change"

# Roll back one migration
alembic downgrade -1
```

---

## Roadmap

- [ ] JWT authentication (login, protected routes)
- [ ] Task priorities and due dates
- [ ] Assign tasks to users (multi-user support)
- [ ] WebSocket endpoint for real-time task updates
- [ ] Deploy public demo (Railway)
- [ ] Rate limiting with slowapi

---

## License

MIT
