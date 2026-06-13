# User Service API

Production-style backend user service built with FastAPI, PostgreSQL, and JWT authentication.

## Demo

![auth-demo](.\assests\auth-demo.gif)

## Architecture

Request flow: **Route → Controller → Service → Repository → Database**

Each layer has a single responsibility, making the codebase easy to test and extend.

## Project Structure

```
app/
  api/
    routes/         # HTTP route definitions
    controllers/    # Request/response orchestration
  services/         # Business logic
  repositories/     # Database access
  models/           # SQLAlchemy ORM models
  schemas/          # Pydantic request/response models
  core/             # Config, security, dependencies, exceptions
  db/               # Database engine and session
alembic/            # Database migrations
tests/              # Pytest test suite
```

## Quick Start

```bash
docker-compose up --build
```

API: http://localhost:8000  
Swagger docs: http://localhost:8000/docs

## Local Development (without Docker)

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -r requirements.txt
cp .env.example .env          # adjust DATABASE_URL for local Postgres
alembic upgrade head
uvicorn app.main:app --reload
```

## API Endpoints

| Method | Endpoint                | Auth | Description              |
| ------ | ----------------------- | ---- | ------------------------ |
| GET    | `/health`               | No   | Health check             |
| POST   | `/api/v1/auth/register` | No   | Register a new user      |
| POST   | `/api/v1/auth/login`    | No   | Login and receive JWT    |
| GET    | `/api/v1/auth/me`       | Yes  | Get current user profile |
| POST   | `/api/v1/users`         | Yes  | Create user              |
| GET    | `/api/v1/users`         | Yes  | List users (paginated)   |
| GET    | `/api/v1/users/{id}`    | Yes  | Get user by ID           |
| PUT    | `/api/v1/users/{id}`    | Yes  | Update user              |
| DELETE | `/api/v1/users/{id}`    | Yes  | Delete user              |

Protected routes require header: `Authorization: Bearer <token>`

## Run Tests

```bash
pip install -r requirements.txt
pytest
```

## 
