# Kanban Board

A simple Kanban board application written in Python — designed to help you track tasks and their progress using the Kanban methodology.

### Overview

This project implements a Kanban workflow system where tasks are organized into columns such as To Do, In Progress, and Done. 

### Stack

##### Main app dependencies:

- Python 3.12+ (running on 3.14-dev)
- FastAPI - Web framework
- SQLAlchemy 2.0 - ORM
- Alembic - Database migrations
- Pydantic - Data validation
- PostgreSQL + asyncpg - Primary database
- [uv](https://docs.astral.sh/uv/) - package manager

##### Dev dependencies:

- Pytest - Testing framework
- Ruff - Linter & Formatter
- aiosqlite - For async testing


### Project structures

```
kanban/
├── backend/
│   ├── api/                    # Endpoints, routers
│   ├── core/                   # Decorators, exception mappers, security, app config
│   ├── database/               # DB provider and UoW
│   ├── dependencies/           # DI
│   ├── exceptions_handlers/    # Exception handlers for the App/SQLAlchemy/Pydantic errors
│   ├── migrations/             # Alembic migrations
│   ├── models/                 # SQLAlchemy models and mixins
│   ├── schemas/                # Pydantic models for the data validation
│   ├── services/               # Business logic via services and database operations via repositories
│   └── main.py                 # App factory & entrypoint
├── tests/                      # Tests
├── pyproject.toml              # Project configuration
└── runner.py                   # App runner
```

### Key Architectural Patterns

- [Generic repository](backend/services/repositories/generic_repo.py) - abstracted database operations to keep repositores DRY.
- [Unit of Work](backend/database/unit_of_work.py) - ensures atomic operations across multiple repositories. Managed via decorators [@transactional](backend/core/decorators/transactional.py) and [@read_only](backend/core/decorators/read_only.py).

- [RBAC](backend/core/security/permission_service.py) - [permission management](backend/dependencies/permission_dep.py) directly in routers. Example:
```python
@router.post("/api/v1/myapi", dependencies=[PermissionDep(RoleEnum.ADMIN)])
```
- [JWT Auth](backend/core/security/user_auth.py) - [stateless](backend/dependencies/auth_dep.py) session management using [HTTP-only cookies](backend/api/v1/auth_router.py).

*Note: Currently app supports only 1 admin per board. Admins can not demote themselves to the different role.*

### Installation

0. Make sure that you have uv as the package manager. If not, you can download it following the [docs](https://docs.astral.sh/uv/getting-started/installation/)

1. Clone the repository
```sh
git clone https://github.com/Kargozaur/kanban
cd kanban
```

2. Sync the dependencies 
```sh
uv venv
uv sync --frozen
```

3. Perform a migration

```
cd backend
uv run alembic upgrade head
cd ..
```

4. Configure the .env file. It should look something like this

```dotenv
# --- POSTGRES deps ---
POSTGRES__USER=<your postgres user>
POSTGRES__PASSWORD=<your postgres password>
POSTGRES__HOST=<your db host>
POSTGRES__DB=kanban
POSTGRES__PORT=<your postgres port in range from 1 to 65535>
POSTGRES__DRIVER=asyncpg
# --- JWT deps ---
TOKEN__SECRET=<your secret key>
TOKEN__TOKEN_TTL=60
TOKEN__ALGORITHM=HS256
# --- Logging deps ---
LOGGING__LEVEL=INFO

# --- sqlalchemy deps ---
SQLALCHEMY__ECHO=false
SQLALCHEMY__ECHO_POOL=false
SQLALCHEMY__POOL_SIZE=5
SQLALCHEMY__MAX_OVERFLOW=10
```
To generate a secret key write 
```sh
openssl rand -hex <desired length>, f.e 32
```
4. Run the app
```sh
uv run runner.py (or python runner.py)
```
*Note: docker file is not yet created, if you want to run it manually via the uvicorn, you should use the following command:*

```sh
uv run uvicorn backend.main:create_app --host 0.0.0.0 --port <desired port> --factory --loop "uvloop"  
```
If you want app to reload on save (If you made some changes yourself) add --reload flag.
Also, you can add workers via adding --workers=<amount of workers> flag.


### Testing

To be able to run the tests, make sure that you have installed dev group dependencies. If not, run
```
uv sync --all-groups
uv run pytest
```

If you want to test a specific module(service) you can run:
```sh
uv run pytest -k test_<service name>
```