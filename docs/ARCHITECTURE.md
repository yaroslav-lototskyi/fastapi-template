# Architecture Overview - Hybrid DI Pattern

Modern FastAPI backend with **Clean Architecture**, **Hybrid DI Pattern**, and **Domain-Driven Design**.

---

## Architecture Layers

```
┌─────────────────────────────────────────────────────────────┐
│                     Presentation Layer                      │
│              (Controllers - HTTP handling)                  │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  UserController      │     PostController            │  │
│  │                                                       │  │
│  │  Hybrid DI:                                          │  │
│  │  • Logger (Singleton) ────► Container                │  │
│  │  • UseCase (per-request) ─► Depends() chain         │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    Application Layer                        │
│                (Use Cases - Business Logic)                 │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  CreateUserUseCase                                    │  │
│  │  GetUserUseCase                                       │  │
│  │  ListUsersUseCase                                     │  │
│  │  DeleteUserUseCase                                    │  │
│  │                                                       │  │
│  │  Depends: IUserRepository (interface)                │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                      Domain Layer                           │
│           (Entities, Interfaces - Pure Business)            │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  UserEntity (domain model)                            │  │
│  │  IUserRepository (interface)                          │  │
│  │                                                       │  │
│  │  Framework agnostic! No SQLAlchemy, no FastAPI       │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                   Infrastructure Layer                      │
│        (DB, External Services - Implementation)             │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  UserRepository (implements IUserRepository)          │  │
│  │  UserModel (SQLAlchemy)                               │  │
│  │  Database connection (AsyncSession)                   │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Container (Singleton services)                       │  │
│  │  • LoggerService                                      │  │
│  │  • EmailService                                       │  │
│  │  • SMSService                                         │  │
│  │  • NotificationService                                │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

## Hybrid DI Pattern

### Concept

Combination of two approaches:

1. **Stateless Services (Singleton)** → `dependency-injector` Container
2. **Stateful Services (per-request)** → FastAPI `Depends()` chain

### Stateless → Singleton (Container)

```python
# src/core/infrastructure/container.py

class ApplicationContainer(containers.DeclarativeContainer):
    # Stateless services - ONE instance for entire app
    logger = providers.Singleton(LoggerService)
    email_service = providers.Singleton(EmailService)
    notification_service = providers.Singleton(NotificationService)
```

**Why Singleton:**
- No internal state
- Thread-safe
- Can be safely shared between requests
- Memory efficient

**Examples:**
- Logger (structlog)
- Email/SMS services
- Cache clients (Redis)
- Configuration services
- External API clients

---

### Stateful → Per-request (Depends)

```python
# src/modules/users/user_providers.py

def get_user_repository(
    db: AsyncSession = Depends(get_db)
) -> IUserRepository:
    return UserRepository(db)

def get_create_user_use_case(
    repo: IUserRepository = Depends(get_user_repository)
) -> CreateUserUseCase:
    return CreateUserUseCase(repo)
```

**Why Per-request:**
- Has internal state (DB transaction)
- NOT thread-safe
- Each request gets isolated instance
- Automatic cleanup after request

**Examples:**
- Database sessions (AsyncSession)
- Repositories (depend on DB session)
- Use Cases (depend on repositories)

---

### Usage in Controller

```python
# src/modules/users/presentation/user_controller.py

@router.post("")
async def create_user(
    dto: CreateUserDto,
    # Stateful (per-request) - via Depends chain
    use_case: CreateUserUseCase = Depends(get_create_user_use_case),
    # Stateless (singleton) - via container
    logger=Depends(get_logger),
    notification=Depends(get_notification),
):
    logger.info("Creating user", email=dto.email)

    # NO manual instantiation!
    user = await use_case.execute(dto)

    await notification.notify(user.id, "Welcome!")

    return user
```

**Dependency Resolution:**

```
HTTP Request
    ↓
FastAPI resolves dependencies
    ↓
For use_case:
    get_create_user_use_case()
        ↓ requires repo
    get_user_repository()
        ↓ requires db
    get_db()
        ↓ creates AsyncSession
        ↓
    UserRepository(session)
        ↓
    CreateUserUseCase(repository)

For logger:
    get_logger()
        ↓ inject from container
    container.logger() ← SINGLETON! One instance!

Controller receives ready dependencies
```

---

## Stack

### Core
- **Python**: 3.11+
- **Framework**: FastAPI (async)
- **DI**: dependency-injector + FastAPI Depends
- **Logging**: structlog (structured JSON logs)

### Database
- **ORM**: SQLAlchemy 2.0 (async)
- **Driver**: asyncpg (PostgreSQL)
- **Migrations**: Alembic
- **Models**: Declarative mappings (typed)
- **DTOs**: Pydantic (separate from models)
- **Session**: per-request AsyncSession via Depends

### Architecture
- **Pattern**: Clean Architecture + DDD
- **Principles**: SOLID
- **Layers**: 4-layer (Domain, Application, Infrastructure, Presentation)
- **Entities**: Separated from DB models

---

## Project Structure

```
src/
├── core/
│   ├── config.py                       # Environment configuration
│   ├── database.py                     # DB setup + per-request session
│   └── infrastructure/
│       ├── container.py                # DI Container (Singleton services)
│       └── logger.py                   # Structured logger service
│
├── modules/
│   ├── users/                          # User module (feature)
│   │   ├── domain/
│   │   │   ├── entities/
│   │   │   │   └── user_entity.py      # Pure domain entity
│   │   │   └── repositories/
│   │   │       └── user_repository_interface.py  # IUserRepository
│   │   │
│   │   ├── application/
│   │   │   ├── dto/
│   │   │   │   └── ...                 # Pydantic DTOs
│   │   │   └── use_cases/
│   │   │       └── ...                 # Business logic
│   │   │
│   │   ├── infrastructure/
│   │   │   └── persistence/
│   │   │       ├── user_model.py       # SQLAlchemy model
│   │   │       └── user_repository.py  # Repository implementation
│   │   │
│   │   ├── presentation/
│   │   │   └── user_controller.py      # FastAPI routes (Hybrid DI)
│   │   │
│   │   └── user_providers.py           # DI providers (per-request)
│   │
│   └── posts/                          # Post module (same structure)
│
└── main.py                             # FastAPI app + DI wiring
```

---

## Key Features

### Clean Architecture
- 4 layers: Domain, Application, Infrastructure, Presentation
- Dependency Inversion Principle
- Framework-agnostic domain layer

### Hybrid DI
- Singleton for stateless services (memory efficient)
- Per-request for stateful services (isolation)
- No tight coupling

### Structured Logging
- JSON logs for production (ELK, DataDog ready)
- Colored console for development
- Context propagation (request_id, user_id)
- Async-friendly

### Type Safety
- SQLAlchemy 2.0 Mapped[] types
- Pydantic DTOs with validation
- Type hints throughout codebase

### Testability
- Dependency override for tests
- Mock repositories via interfaces
- Container override for singleton services

---

## Data Flow

### How data flows through the system:

1. **HTTP Request** → `user_controller.py`
2. **Controller** calls `CreateUserUseCase` (DI via Depends)
3. **Use Case** calls `UserRepository.create()` (DI via Depends)
4. **Repository** works with `UserModel` (SQLAlchemy)
5. **Repository** converts `UserModel` → `UserEntity`
6. **Use Case** returns `UserResponseDto` (Pydantic)
7. **Controller** logs via `LoggerService` (Singleton from Container)
8. **Controller** calls `NotificationService` (Singleton from Container)
9. **Response** returned to client

### Dependency Flow:

```
Container (Singleton services)
    ├── LoggerService ────────┐
    ├── EmailService          │
    ├── SMSService            │
    └── NotificationService   │
                              │
                              ▼
Controller ◄────────────── @inject
    ├── Depends(get_logger) ──────► LoggerService (Singleton)
    ├── Depends(get_notification) ► NotificationService (Singleton)
    └── Depends(get_use_case)
            ↓
        CreateUserUseCase
            ↓ Depends(get_repository)
        UserRepository
            ↓ Depends(get_db)
        AsyncSession (per-request)
```

---

## Benefits

This architecture provides:
- Easy to scale (add modules)
- Easy to test (DI + interfaces)
- Optimized (Singleton + per-request)
- Professional logging
- Follows SOLID principles

**Production-ready!**
