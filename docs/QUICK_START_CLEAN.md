# Quick Start - Clean Architecture

FastAPI project with **Clean Architecture**, **DDD**, and **SOLID principles**.

---

## Features

- Clean Architecture (4 layers)
- Domain-Driven Design (DDD)
- SOLID principles
- Use Cases pattern
- Repository pattern
- Dependency Injection
- Feature modules

---

## Project Structure

```
src/
├── core/                      # Shared infrastructure
│   ├── domain/               # Base entities, repositories
│   ├── application/          # Base use cases
│   └── infrastructure/       # Database, config
│
├── modules/                  # Feature modules
│   └── users/               # User feature
│       ├── domain/          # Business entities & rules
│       │   ├── entities/    # UserEntity
│       │   └── repositories/  # IUserRepository (interface)
│       ├── application/     # Use cases & DTOs
│       │   ├── dto/        # CreateUserDto, UserResponseDto
│       │   └── use_cases/   # CreateUserUseCase, GetUserUseCase
│       ├── infrastructure/  # Database implementation
│       │   └── persistence/  # UserModel, UserRepository
│       ├── presentation/    # HTTP layer
│       │   └── user_controller.py
│       └── user_providers.py  # Dependency Injection
│
└── main.py                  # Entry point
```

---

## Quick Start

### 1. Start PostgreSQL

```bash
make docker-dev-up
```

### 2. Run Migrations

```bash
# Remove old migrations (if any)
rm -rf alembic/versions/*

# Create new migration
make dev-migration message="Initial migration"

# Apply migration
make dev-migrate
```

### 3. Seed Database

```bash
make dev-seed
```

### 4. Start Application

```bash
make dev-start

# Open: http://localhost:8000/docs
```

---

## Testing API

### Create User

```bash
curl -X POST http://localhost:8000/api/users \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "username": "johndoe",
    "full_name": "John Doe"
  }'
```

### List Users

```bash
curl http://localhost:8000/api/users
```

### Get User by ID

```bash
curl http://localhost:8000/api/users/1
```

---

## Architecture Comparison

### Simple Approach

```
src/users/
├── models.py       # SQLAlchemy model
├── schemas.py      # Pydantic schemas
├── service.py      # Business logic
└── routes.py       # FastAPI routes
```

**Problems:**
- Everything tied to SQLAlchemy
- Hard to test
- Hard to change database
- service.py does too many things

### Clean Architecture

```
src/modules/users/
├── domain/                    # Business logic (framework-agnostic!)
│   ├── entities/             # UserEntity (pure business)
│   └── repositories/         # IUserRepository (interface)
├── application/              # Use cases
│   ├── dto/                  # DTOs for API
│   └── use_cases/            # Each use case = ONE thing
├── infrastructure/           # Technical details
│   └── persistence/          # UserModel, UserRepository
└── presentation/             # HTTP layer
    └── user_controller.py
```

**Benefits:**
- Domain layer framework-independent
- Easy to test (mock repositories)
- Easy to change DB (change only repository)
- Single Responsibility Principle
- Dependency Inversion

---

## Dependency Injection

### How It Works

```python
# user_providers.py
def get_user_repository(db: AsyncSession = Depends(get_db)):
    return UserRepository(db)

def get_create_user_use_case(
    repo: IUserRepository = Depends(get_user_repository)
):
    return CreateUserUseCase(repo)

# user_controller.py
@router.post("")
async def create_user(
    dto: CreateUserDto,
    use_case: CreateUserUseCase = Depends(get_create_user_use_case)
):
    return await use_case.execute(dto)
```

**DI Chain:**
```
Controller → Use Case → Repository → Database
     ↑          ↑           ↑           ↑
   Depends → Depends → Depends → get_db()
```

---

## Data Flow

### Create User Request:

```
1. HTTP Request
   ↓
2. UserController.create_user()
   ↓
3. CreateUserUseCase.execute(dto)
   ├── Validate business rules
   ├── Create UserEntity (domain)
   ├── Call repository.create()
   └── Return UserResponseDto
   ↓
4. UserRepository.create()
   ├── Convert UserEntity → UserModel
   ├── Save to database (SQLAlchemy)
   ├── Convert UserModel → UserEntity
   └── Return UserEntity
   ↓
5. Use Case converts to DTO
   ↓
6. HTTP Response
```

---

## Next Steps

### 1. Explore Structure

```bash
# Start with domain layer
cat src/modules/users/domain/entities/user_entity.py
cat src/modules/users/domain/repositories/user_repository_interface.py

# Then application layer
cat src/modules/users/application/use_cases/create_user_use_case.py

# Then infrastructure
cat src/modules/users/infrastructure/persistence/user_repository.py
```

### 2. Read Documentation

- [ARCHITECTURE.md](ARCHITECTURE.md) - Architecture overview
- [CLEAN_ARCHITECTURE.md](CLEAN_ARCHITECTURE.md) - Clean Architecture details

### 3. Add New Feature

Copy users module structure and create your own module (e.g., posts, comments).

---

## When to Use

### Use Clean Architecture:
- Large projects
- Enterprise applications
- Need to scale
- Multiple developers
- High testability required

### Simple approach sufficient:
- Small scripts
- Prototypes
- MVPs
- 1-2 day projects

---

## Trade-offs

**Clean Architecture:**
- ~2.5x more code
- More complex structure
- But: easier to test, maintain, and scale

**Simple Approach:**
- Less code
- Faster to start
- But: harder to test and maintain long-term

---

## Conclusion

You now have:
- Modern Python backend structure
- Clean Architecture implementation
- SOLID principles
- Domain-Driven Design
- Production-ready foundation
