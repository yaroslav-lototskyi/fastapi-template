# Clean Architecture + DDD

FastAPI project with **Clean Architecture**, **Domain-Driven Design (DDD)**, and **SOLID principles**.

---

## Architecture

```
┌─────────────────────────────────────────┐
│        Presentation Layer               │  ← FastAPI Controllers (HTTP)
│  (Controllers, DTOs, Routes)            │
├─────────────────────────────────────────┤
│        Application Layer                │  ← Use Cases (Business logic)
│  (Use Cases, Application DTOs)          │
├─────────────────────────────────────────┤
│        Domain Layer                     │  ← Business entities & rules
│  (Entities, Repository Interfaces)      │
├─────────────────────────────────────────┤
│        Infrastructure Layer             │  ← Technical details
│  (Database, External APIs, etc.)        │
└─────────────────────────────────────────┘
```

### Dependency Rule

```
Presentation → Application → Domain
                          ↑
Infrastructure ──────────┘

- Inner layers DON'T know about outer layers
- Domain layer depends on NOTHING
- Dependencies point INWARD only
```

---

## Project Structure

```
src/
├── core/                           # Shared core (base classes)
│   ├── domain/
│   │   ├── entities/
│   │   │   └── base_entity.py     # BaseEntity
│   │   └── repositories/
│   │       └── base_repository.py # BaseRepository interface
│   ├── application/
│   │   └── use_cases/
│   │       └── base_use_case.py   # BaseUseCase
│   └── infrastructure/
│       └── database.py             # Database config
│
├── modules/                        # Feature modules
│   └── users/                      # User feature module
│       ├── domain/                 # Domain Layer
│       │   ├── entities/
│       │   │   └── user_entity.py          # UserEntity (business object)
│       │   └── repositories/
│       │       └── user_repository_interface.py  # IUserRepository (contract)
│       │
│       ├── application/            # Application Layer
│       │   ├── dto/
│       │   │   ├── create_user_dto.py      # Input DTO
│       │   │   ├── update_user_dto.py      # Input DTO
│       │   │   └── user_response_dto.py    # Output DTO
│       │   └── use_cases/
│       │       ├── create_user_use_case.py # Business logic
│       │       ├── get_user_use_case.py
│       │       ├── list_users_use_case.py
│       │       └── delete_user_use_case.py
│       │
│       ├── infrastructure/         # Infrastructure Layer
│       │   └── persistence/
│       │       ├── user_model.py           # SQLAlchemy model
│       │       └── user_repository.py      # Repository implementation
│       │
│       ├── presentation/           # Presentation Layer
│       │   └── user_controller.py          # FastAPI routes
│       │
│       └── user_providers.py       # Dependency Injection
│
└── main.py                         # Application entry point
```

---

## Core Patterns

### 1. Domain Entity

```python
# user_entity.py (domain)
class UserEntity(BaseEntity):
    def __init__(self, email: str, username: str):
        self.email = email
        self.username = username

    def deactivate(self) -> None:
        self.is_active = False
```

```python
# user_model.py (database - SQLAlchemy)
class UserModel(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255))
```

### 2. Repository Pattern

```python
# user_repository_interface.py (domain)
class IUserRepository(BaseRepository[UserEntity]):
    @abstractmethod
    async def find_by_id(self, id: int) -> Optional[UserEntity]:
        pass

# user_repository.py (infrastructure)
class UserRepository(IUserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def find_by_id(self, id: int) -> Optional[UserEntity]:
        result = await self.session.execute(
            select(UserModel).where(UserModel.id == id)
        )
        model = result.scalar_one_or_none()
        return self._model_to_entity(model) if model else None
```

### 3. Use Case

```python
# create_user_use_case.py
class CreateUserUseCase(BaseUseCase[CreateUserDto, UserResponseDto]):
    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository

    async def execute(self, input_dto: CreateUserDto) -> UserResponseDto:
        # 1. Validate
        if await self.user_repository.email_exists(input_dto.email):
            raise HTTPException(
                status_code=400,
                detail="Email already exists"
            )

        # 2. Create entity
        user_entity = UserEntity(
            email=input_dto.email,
            username=input_dto.username
        )

        # 3. Save
        created_user = await self.user_repository.create(user_entity)

        # 4. Return DTO
        return self._entity_to_dto(created_user)
```

### 4. Controller

```python
# user_controller.py
router = APIRouter(prefix="/users")

@router.post("", status_code=201)
async def create_user(
    dto: CreateUserDto,
    use_case: CreateUserUseCase = Depends(get_create_user_use_case),
) -> UserResponseDto:
    return await use_case.execute(dto)

@router.get("/{user_id}")
async def get_user(
    user_id: int,
    use_case: GetUserUseCase = Depends(get_get_user_use_case),
) -> UserResponseDto:
    return await use_case.execute(user_id)
```

### 5. Dependency Injection

```python
# user_providers.py
def get_user_repository(
    db: AsyncSession = Depends(get_db)
) -> IUserRepository:
    return UserRepository(db)

def get_create_user_use_case(
    repo: IUserRepository = Depends(get_user_repository)
) -> CreateUserUseCase:
    return CreateUserUseCase(repo)

# main.py
app = FastAPI()
app.include_router(users_router, prefix="/api")
```

---

## SOLID Principles

### 1. Single Responsibility Principle (SRP)

```python
# Bad - one class does everything
class UserService:
    def create_user(self): pass
    def validate_user(self): pass
    def save_to_db(self): pass
    def send_email(self): pass

# Good - each class does one thing
class CreateUserUseCase:
    def execute(self): pass  # Only business logic for creation

class UserRepository:
    def create(self): pass  # Only database persistence

class EmailService:
    def send(self): pass  # Only email sending
```

### 2. Open/Closed Principle (OCP)

```python
# Open for extension, closed for modification
class BaseRepository(ABC):
    @abstractmethod
    async def create(self, entity): pass

class UserRepository(BaseRepository):  # Extend, don't modify
    async def create(self, entity): pass

class OrderRepository(BaseRepository):  # New capabilities
    async def create(self, entity): pass
```

### 3. Liskov Substitution Principle (LSP)

```python
# Subclass can replace base class
def process_entity(repo: BaseRepository, entity):
    return repo.create(entity)

# Works with any repository
process_entity(UserRepository(), user)
process_entity(OrderRepository(), order)
```

### 4. Interface Segregation Principle (ISP)

```python
# Bad - large interface
class IRepository:
    def create(self): pass
    def read(self): pass
    def update(self): pass
    def delete(self): pass
    def export_to_csv(self): pass  # Not everyone needs this!

# Good - small interfaces
class IReadRepository:
    def find_by_id(self): pass

class IWriteRepository:
    def create(self): pass

class IUserRepository(IReadRepository, IWriteRepository):
    # Uses only what's needed
    pass
```

### 5. Dependency Inversion Principle (DIP)

**Most important for Clean Architecture!**

```python
# Bad - use case depends on concrete implementation
class CreateUserUseCase:
    def __init__(self):
        self.repo = UserRepository()  # Hard dependency!

# Good - use case depends on abstraction
class CreateUserUseCase:
    def __init__(self, user_repository: IUserRepository):  # Interface!
        self.user_repository = user_repository

# Can substitute any implementation:
use_case = CreateUserUseCase(UserRepository())  # SQLAlchemy
use_case = CreateUserUseCase(MockUserRepository())  # For testing
use_case = CreateUserUseCase(MongoUserRepository())  # MongoDB
```

---

## Benefits

### 1. Testability

```python
# Unit test use case - without DB!
def test_create_user():
    # Arrange
    mock_repo = MockUserRepository()  # Fake repository
    use_case = CreateUserUseCase(mock_repo)
    dto = CreateUserDto(email="test@test.com", username="test")

    # Act
    result = await use_case.execute(dto)

    # Assert
    assert result.email == "test@test.com"
    # No real DB queries!
```

### 2. Database Migration

```python
# Migrating from PostgreSQL to MongoDB - change only repository!

# Before:
class UserRepository(IUserRepository):
    def __init__(self, session: AsyncSession):  # PostgreSQL
        ...

# After:
class MongoUserRepository(IUserRepository):
    def __init__(self, client: MongoClient):  # MongoDB
        ...

# Use cases remain UNCHANGED!
```

### 3. Framework Migration

```python
# Migrating from FastAPI to Flask - change only controller!

# Domain, Application, Infrastructure - NO CHANGES!
# Only presentation layer:

# Before: FastAPI
@router.post("")
async def create_user(dto: CreateUserDto):
    return await use_case.execute(dto)

# After: Flask
@app.route("", methods=["POST"])
def create_user():
    dto = CreateUserDto(**request.json)
    return use_case.execute(dto)
```

---

## Adding New Module

### 1. Create structure:

```bash
mkdir -p src/modules/posts/{domain/{entities,repositories},application/{dto,use_cases},infrastructure/persistence,presentation}
```

### 2. Domain Layer:

```python
# domain/entities/post_entity.py
class PostEntity(BaseEntity):
    def __init__(self, title: str, content: str):
        self.title = title
        self.content = content

# domain/repositories/post_repository_interface.py
class IPostRepository(BaseRepository[PostEntity]):
    @abstractmethod
    async def find_by_title(self, title: str) -> Optional[PostEntity]:
        pass
```

### 3. Application Layer:

```python
# application/dto/create_post_dto.py
class CreatePostDto(BaseModel):
    title: str
    content: str

# application/use_cases/create_post_use_case.py
class CreatePostUseCase(BaseUseCase[CreatePostDto, PostResponseDto]):
    def __init__(self, post_repository: IPostRepository):
        self.post_repository = post_repository

    async def execute(self, input_dto: CreatePostDto) -> PostResponseDto:
        # Business logic here
        pass
```

### 4. Infrastructure Layer:

```python
# infrastructure/persistence/post_model.py
class PostModel(Base):
    __tablename__ = "posts"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255))

# infrastructure/persistence/post_repository.py
class PostRepository(IPostRepository):
    def __init__(self, session: AsyncSession):
        self.session = session
    # Implement interface methods
```

### 5. Presentation Layer:

```python
# presentation/post_controller.py
router = APIRouter(prefix="/posts")

@router.post("")
async def create_post(
    dto: CreatePostDto,
    use_case: CreatePostUseCase = Depends(get_create_post_use_case),
):
    return await use_case.execute(dto)

# post_providers.py
def get_create_post_use_case(
    repo: IPostRepository = Depends(get_post_repository)
) -> CreatePostUseCase:
    return CreatePostUseCase(repo)
```

### 6. Register in main.py:

```python
from src.modules.posts.presentation import router as posts_router

app.include_router(posts_router, prefix="/api")
```

---

## Comparison

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
│   ├── entities/             # UserEntity (pure business logic)
│   └── repositories/         # IUserRepository (interface)
├── application/              # Use cases (apply business logic)
│   ├── dto/                  # DTOs for API
│   └── use_cases/            # Each use case does ONE thing
├── infrastructure/           # Technical details
│   └── persistence/          # UserModel (SQLAlchemy), UserRepository
└── presentation/             # HTTP layer
    └── user_controller.py    # FastAPI routes
```

**Benefits:**
- Domain layer framework-independent
- Easy to test (mock repositories)
- Easy to change DB (change only repository)
- Each use case has single responsibility (SRP)
- Dependency Inversion (depend on interfaces)

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

## Conclusion

Clean Architecture provides:
- Scalability
- Testability
- Flexibility
- Clear separation of concerns

**Trade-off:** ~2.5x more code, but much easier to maintain and scale.
