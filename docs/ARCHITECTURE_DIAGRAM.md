# Architecture Diagrams

Visual representation of the Clean Architecture implementation.

---

## Clean Architecture Layers

```
┌─────────────────────────────────────────────────────────┐
│                  PRESENTATION LAYER                      │
│            (Frameworks & Drivers - Outermost)            │
│  ┌───────────────────────────────────────────────────┐  │
│  │  UserController (FastAPI Routes)                  │  │
│  │  - POST /users  → CreateUserUseCase               │  │
│  │  - GET /users   → ListUsersUseCase                │  │
│  │  - GET /users/1 → GetUserUseCase                  │  │
│  └───────────────────┬───────────────────────────────┘  │
└────────────────────────┼────────────────────────────────┘
                         │ HTTP Request/Response
                         │ (DTOs)
┌────────────────────────┼────────────────────────────────┐
│                  APPLICATION LAYER                       │
│             (Use Cases - Business Rules)                 │
│  ┌───────────────────▼───────────────────────────────┐  │
│  │  CreateUserUseCase                                │  │
│  │  1. Validate (email unique?)                      │  │
│  │  2. Create UserEntity                             │  │
│  │  3. Save via IUserRepository                      │  │
│  │  4. Return DTO                                    │  │
│  └───────────────────┬───────────────────────────────┘  │
│  ┌───────────────────▼───────────────────────────────┐  │
│  │  DTOs (CreateUserDto, UserResponseDto)            │  │
│  └───────────────────────────────────────────────────┘  │
└────────────────────────┼────────────────────────────────┘
                         │ Uses Interface
                         │ (IUserRepository)
┌────────────────────────┼────────────────────────────────┐
│                    DOMAIN LAYER                          │
│           (Entities - Core Business Logic)               │
│  ┌───────────────────▼───────────────────────────────┐  │
│  │  IUserRepository (Interface)                      │  │
│  │  - create(entity)                                 │  │
│  │  - find_by_id(id)                                 │  │
│  │  - email_exists(email)                            │  │
│  └───────────────────────────────────────────────────┘  │
│  ┌───────────────────────────────────────────────────┐  │
│  │  UserEntity (Pure Business Object)                │  │
│  │  - email, username, full_name                     │  │
│  │  - deactivate()  ← Business logic method         │  │
│  │  - can_login()   ← Business rule                 │  │
│  └───────────────────────────────────────────────────┘  │
└────────────────────────┬────────────────────────────────┘
                         │ Interface implemented by ↓
┌────────────────────────┼────────────────────────────────┐
│                 INFRASTRUCTURE LAYER                     │
│          (Database, External Services, etc.)             │
│  ┌───────────────────▼───────────────────────────────┐  │
│  │  UserRepository (implements IUserRepository)      │  │
│  │  - Uses SQLAlchemy                                │  │
│  │  - Converts Entity ↔ Model                        │  │
│  └───────────────────┬───────────────────────────────┘  │
│  ┌───────────────────▼───────────────────────────────┐  │
│  │  UserModel (SQLAlchemy ORM)                       │  │
│  │  __tablename__ = "users"                          │  │
│  │  - Mapped columns                                 │  │
│  └───────────────────┬───────────────────────────────┘  │
└────────────────────────┼────────────────────────────────┘
                         ▼
                 ┌─────────────┐
                 │  PostgreSQL  │
                 │   Database   │
                 └─────────────┘
```

---

## Dependency Flow (Dependency Inversion Principle)

```
┌─────────────────────────────────────────────────────────┐
│  DEPENDENCIES FLOW INWARD (NEVER OUTWARD!)              │
│                                                          │
│  Presentation ──────────────┐                           │
│                             ▼                           │
│          Application ────────────► Domain               │
│                             ▲                           │
│  Infrastructure ────────────┘                           │
│                                                          │
│  Infrastructure depends on Domain (not vice versa!)     │
└─────────────────────────────────────────────────────────┘
```

---

## Dependency Injection Chain

```
HTTP Request
    │
    ▼
┌────────────────────────────────────────┐
│  FastAPI Depends() System              │
│  (Automatic DI)                        │
└────────────────┬───────────────────────┘
                 │
    ┌────────────┼────────────┬───────────────┐
    │            │            │               │
    ▼            ▼            ▼               ▼
┌─────────┐  ┌─────────┐  ┌──────────┐  ┌────────┐
│get_db() │→│get_user_│→│get_create│→│create_ │
│         │  │repository│ │_user_use_│  │user()  │
│AsyncSess│  │         │  │case      │  │        │
└─────────┘  └─────────┘  └──────────┘  └────────┘
     │            │             │             │
     ▼            ▼             ▼             ▼
 Database    UserRepo    CreateUser    Controller
 Session    (implements  UseCase       (calls
            IUserRepo)   (business    use case)
                         logic)
```

---

## Module Structure

```
┌──────────────────────────────────────────────────────────┐
│  UserModule (Feature Module)                             │
│                                                           │
│  providers: [                                             │
│    get_user_repository() → UserRepository                │
│    get_create_user_use_case() → CreateUserUseCase        │
│    get_get_user_use_case() → GetUserUseCase              │
│  ]                                                        │
│                                                           │
│  controllers: [                                           │
│    UserController (routes)                                │
│  ]                                                        │
│                                                           │
│  exports: []                                              │
└──────────────────────────────────────────────────────────┘

               │ Registered in │
               ▼               ▼

┌──────────────────────────────────────────────────────────┐
│  main.py (Application)                                   │
│                                                           │
│  app = FastAPI()                                          │
│  app.include_router(users_router, prefix="/api")         │
└──────────────────────────────────────────────────────────┘
```

---

## Request Flow Example: Create User

```
1. HTTP POST /api/users
   Body: { "email": "john@test.com", "username": "john" }
        │
        ▼
2. UserController.create_user()
   - Receives CreateUserDto
   - DI injects CreateUserUseCase
        │
        ▼
3. CreateUserUseCase.execute(dto)
   ┌────────────────────────────────────────┐
   │  Business Logic:                       │
   │  ✓ Check if email exists               │
   │  ✓ Check if username exists            │
   │  ✓ Create UserEntity (domain object)   │
   │  ✓ Call repository.create(entity)      │
   │  ✓ Convert entity → DTO                │
   └────────────┬───────────────────────────┘
                │ Calls IUserRepository
                ▼
4. UserRepository.create(entity)
   ┌────────────────────────────────────────┐
   │  Database Operations:                  │
   │  ✓ Convert UserEntity → UserModel      │
   │  ✓ session.add(model)                  │
   │  ✓ session.flush()                     │
   │  ✓ Convert UserModel → UserEntity      │
   │  ✓ Return entity                       │
   └────────────┬───────────────────────────┘
                │ SQLAlchemy
                ▼
5. PostgreSQL
   INSERT INTO users (email, username, ...) VALUES (...)
        │
        ▼
6. Return to Use Case → Convert to DTO → Return to Controller
        │
        ▼
7. HTTP 201 Created
   Body: { "id": 1, "email": "john@test.com", ... }
```

---

## Why This Architecture? Testability!

### Testing Use Case (Unit Test):

```python
# NO DATABASE NEEDED!

def test_create_user():
    # Mock repository (fake implementation)
    mock_repo = MockUserRepository()  # ← Implements IUserRepository

    # Create use case with mock
    use_case = CreateUserUseCase(mock_repo)

    # Test business logic
    dto = CreateUserDto(email="test@test.com", username="test")
    result = await use_case.execute(dto)

    assert result.email == "test@test.com"
    # Fast test, no DB, no frameworks!
```

### Testing Controller (Integration Test):

```python
# WITH DATABASE

async def test_create_user_endpoint(client: AsyncClient):
    response = await client.post("/api/users", json={
        "email": "test@test.com",
        "username": "test"
    })

    assert response.status_code == 201
    # Full integration test
```

---

## Comparison: Simple vs Clean Architecture

### Simple Approach:

```
src/users/
├── models.py     ← SQLAlchemy (DB details)
│   └── User
│
├── service.py    ← Business logic + DB operations (mixed!)
│   └── UserService
│       ├── create_user()       # Business logic
│       ├── _validate()         # Business logic
│       └── session.add()       # DB operation
│
├── schemas.py    ← Pydantic DTOs
│   └── UserCreate, UserResponse
│
└── routes.py     ← FastAPI routes
    └── @router.post("")
        └── service.create_user()

Problems:
- Business logic mixed with DB
- Hard to test (need DB)
- Hard to change DB
- One big service class
```

### Clean Architecture:

```
src/modules/users/
│
├── domain/                       ← Pure business logic
│   ├── entities/
│   │   └── user_entity.py       # Business object (NO SQLAlchemy!)
│   │       ├── deactivate()      # Business method
│   │       └── can_login()       # Business rule
│   │
│   └── repositories/
│       └── user_repository_interface.py  # Contract (interface)
│
├── application/                  ← Use cases (orchestration)
│   ├── dto/
│   │   └── create_user_dto.py   # Input/Output
│   │
│   └── use_cases/
│       └── create_user_use_case.py
│           ├── Validate business rules
│           ├── Create entity
│           ├── Call repository (interface!)
│           └── Return DTO
│
├── infrastructure/               ← Technical details
│   └── persistence/
│       ├── user_model.py        # SQLAlchemy model
│       └── user_repository.py   # Implements interface
│           ├── Convert entity ↔ model
│           └── DB operations
│
└── presentation/                 ← HTTP layer
    └── user_controller.py       # FastAPI routes
        └── @router.post("")
            └── use_case.execute()

Benefits:
- Separation of concerns (SRP)
- Easy to test (mock repositories)
- Easy to change DB (new repository)
- Clear dependencies (DIP)
- Scalable structure
```

---

## Key Takeaways

1. **Dependencies flow INWARD**
   - Outer layers depend on inner layers
   - Inner layers know NOTHING about outer layers

2. **Domain is pure business logic**
   - No framework dependencies
   - No database dependencies
   - Only business rules and entities

3. **Use Cases orchestrate**
   - One use case = one business operation
   - Single Responsibility Principle

4. **Repository abstracts data access**
   - Domain defines interface (IRepository)
   - Infrastructure implements (Repository)
   - Use cases depend on interface, not implementation

5. **DI makes it all work**
   - FastAPI Depends() for automatic dependency injection
   - Automatic wiring of dependencies
   - Easy to test with mocks
