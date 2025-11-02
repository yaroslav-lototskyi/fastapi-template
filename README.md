# FastAPI Clean Architecture Template

Modern Python backend with **Clean Architecture**, **Hybrid DI pattern**, and **Structured logging**.

---

## 🎯 Stack

### Core
- **Python 3.11+**
- **FastAPI** - Modern async web framework
- **dependency-injector** - IoC Container for singleton services
- **structlog** - Structured JSON logging

### Database
- **SQLAlchemy 2.0** - Async ORM
- **asyncpg** - PostgreSQL async driver
- **Alembic** - Database migrations
- **Pydantic** - Data validation & DTOs

### Architecture
- **Clean Architecture** (4 layers)
- **Hybrid DI Pattern** (Singleton + per-request)
- **Domain-Driven Design** (DDD)
- **SOLID Principles**

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Poetry
- Docker & Docker Compose
- PostgreSQL (via Docker)

### Installation

```bash
# 1. Clone repository
git clone <repo-url>
cd fastapi-template

# 2. Install dependencies
poetry install

# 3. Start Docker services (PostgreSQL, Redis, etc.)
make docker-dev-up

# 4. Run migrations and seed database
make dev-setup

# 5. Start application
make dev-start
```

### Access Points

- **API Documentation**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health
- **pgAdmin**: http://localhost:5050
- **MailHog**: http://localhost:8025

---

## 📁 Project Structure

```
src/
├── core/                        # Core infrastructure
│   ├── config.py               # Application settings
│   ├── database.py             # Database setup
│   └── infrastructure/
│       ├── container.py        # DI Container
│       └── logger.py           # Structured logging
│
├── modules/                    # Feature modules
│   ├── users/
│   │   ├── domain/            # Business entities & interfaces
│   │   ├── application/       # Use cases & DTOs
│   │   ├── infrastructure/    # Database models & repositories
│   │   ├── presentation/      # API controllers
│   │   ├── dependencies.py    # Module dependencies
│   │   └── user_providers.py  # DI providers
│   │
│   └── posts/
│       └── ...
│
└── main.py                     # Application entry point

docker/
├── development/               # Dev environment
│   ├── docker-compose.yml
│   └── .env.development
└── test/                      # Test environment
    ├── docker-compose.yml
    └── .env.test

scripts/
└── seed.py                    # Database seeding
```

---

## 🏗️ Architecture

### Clean Architecture Layers

1. **Presentation Layer** - API controllers, HTTP handling
2. **Application Layer** - Use cases, business orchestration
3. **Domain Layer** - Business entities, interfaces (framework-agnostic)
4. **Infrastructure Layer** - Database, external services, implementations

### Hybrid DI Pattern

**Stateless Services (Singleton)** - via `dependency-injector`:
- Logger
- Email/SMS services
- Notification services

**Stateful Services (Per-request)** - via `FastAPI Depends`:
- Database sessions
- Repositories
- Use cases

### Example Controller

```python
@router.post("", response_model=UserResponseDto)
async def create_user(
    dto: CreateUserDto,
    use_case: CreateUserUseCase = Depends(get_create_user_use_case),  # Per-request
    logger=Depends(get_logger),  # Singleton
):
    logger.info("Creating user", email=dto.email)
    user = await use_case.execute(dto)
    logger.info("User created", user_id=user.id)
    return user
```

---

## 🐳 Docker Commands

### Development

```bash
make docker-dev-up          # Start dev services
make dev-setup              # Run migrations + seed data
make dev-start              # Start FastAPI app
make docker-dev-logs        # View logs
make docker-dev-down        # Stop services
```

### Test

```bash
make docker-test-up         # Start test services
make test-setup             # Prepare test database
make test-run               # Run tests
make test-cov               # Run tests with coverage
```

### Database

```bash
make dev-migration message="description"  # Create migration
make dev-migrate            # Apply migrations
make dev-seed               # Seed database
make dev-setup              # Migrations + seeds
```

---

## 📚 Available Commands

Run `make help` to see all available commands:

```bash
make help
```

### Key Commands

| Command | Description |
|---------|-------------|
| `make install` | Install dependencies |
| `make docker-dev-up` | Start dev Docker services |
| `make dev-setup` | Setup database (migrations + seeds) |
| `make dev-start` | Start application with hot reload |
| `make test-run` | Run tests |
| `make format` | Format code (black + ruff) |
| `make lint` | Lint code |

---

## 🧪 Testing the API

### Using curl

```bash
# List users
curl http://localhost:8000/api/users | jq

# Get user by ID
curl http://localhost:8000/api/users/1 | jq

# Create user
curl -X POST http://localhost:8000/api/users \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "username": "testuser",
    "full_name": "Test User"
  }' | jq

# Create post
curl -X POST http://localhost:8000/api/posts \
  -H "Content-Type: application/json" \
  -d '{
    "title": "My Post",
    "content": "Post content here",
    "author_id": 1,
    "is_published": true
  }' | jq
```

### Using Swagger UI

Open http://localhost:8000/docs for interactive API testing.

---

## 📊 Database Seeding

Seeds create test data:
- **5 users**: admin, john, jane, bob, alice (1 inactive)
- **10 posts**: 9 published, 1 draft

```bash
make dev-seed
```

---

## 🔧 Development

### Code Quality

```bash
make format    # Format code
make lint      # Check code quality
make clean     # Remove cache files
```

### Project Structure

- Each module follows Clean Architecture
- Dependencies point inward (Domain ← Application ← Presentation)
- Domain layer is framework-agnostic
- Use cases orchestrate business logic
- Controllers are thin HTTP handlers

---

## 📖 Documentation

- [Quick Start](docs/QUICK_START_CLEAN.md)
- [Architecture Guide](docs/ARCHITECTURE.md)
- [Clean Architecture](docs/CLEAN_ARCHITECTURE.md)
- [Docker Setup](docker/README.md)
- [Database Seeds](scripts/README.md)

---

## 🤝 Contributing

1. Follow Clean Architecture principles
2. Keep domain layer pure (no framework imports)
3. Use dependency injection
4. Write tests for use cases
5. Use structured logging
6. Follow Python style guide (black + ruff)

---

## 📝 License

MIT
