# Learning Guide

Step-by-step guide to understanding the FastAPI Clean Architecture project.

---

## File Study Order

### Stage 1: Configuration & Basics (Day 1-3)

#### 1. `pyproject.toml`

Configuration file for Poetry (Python dependency manager).

**Key dependencies:**
```toml
[tool.poetry.dependencies]
python = "^3.11"           # Python version
fastapi = "^0.115.0"       # Main framework
sqlalchemy = "^2.0.36"     # ORM
```

**Experiment:**
```bash
# Add new dependency
poetry add requests

# View all dependencies
poetry show

# Create requirements.txt for pip
poetry export -f requirements.txt --output requirements.txt
```

---

#### 2. `src/core/config.py`

Application settings via environment variables.

**Key features:**
- `BaseSettings` - automatically loads .env
- `@lru_cache` - singleton pattern
- `Field()` - validation with default values
- Type hints for all fields

**Experiment:**
```python
# Try in Python REPL:
from src.core.config import get_settings

settings = get_settings()
print(settings.database_url)
print(settings.debug)
```

---

#### 3. `.env` and `.env.example`

Environment variables for configuration.

**Important:**
- Never commit `.env` to git
- `.env.example` - template for team
- All variables automatically loaded into `Settings`

**Experiment:**
Change `DEBUG=False` and see how it affects SQL logs.

---

### Stage 2: Database Setup (Day 4-6)

#### 4. `src/core/database.py`

SQLAlchemy async ORM configuration.

**Key concepts:**
```python
# Async engine (for async/await)
engine = create_async_engine(settings.database_url)

# Session factory
AsyncSessionLocal = async_sessionmaker(engine)

# Dependency injection
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session
```

**Experiment:**
Add `echo=True` to engine - see all SQL queries in console.

---

#### 5. SQLAlchemy Models

**Key features:**
```python
class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
```

- `Mapped[type]` - type-safe columns
- `mapped_column()` - column configuration
- `server_default=func.now()` - database-level default
- `__repr__()` - convenient console output

**Experiment:**
```python
# Create migration for new column
# 1. Add to User model:
bio: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

# 2. Create migration:
poetry run alembic revision --autogenerate -m "Add bio field"

# 3. Apply:
poetry run alembic upgrade head
```

---

### Stage 3: Schemas & Validation (Day 7-9)

#### 6. Pydantic Schemas

DTOs for validation and serialization.

**Architecture pattern:**
```
UserBase        # Base fields
  ↓
UserCreate      # For creation (all required)
UserUpdate      # For updates (all optional)
UserResponse    # For responses (+ additional fields)
```

**Key Pydantic features:**
```python
# Email validation
email: EmailStr  # Automatically validates format

# Min/max length
username: str = Field(..., min_length=3, max_length=100)

# Optional fields
full_name: Optional[str] = None

# ORM configuration
model_config = ConfigDict(from_attributes=True)
```

**Experiment:**
```python
# Try in Python REPL:
from src.modules.users.application.dto import CreateUserDto

# Valid
user = CreateUserDto(
    email="test@example.com",
    username="john"
)

# Invalid (validation error)
try:
    user = CreateUserDto(
        email="invalid",
        username="ab"  # Less than 3 characters
    )
except Exception as e:
    print(e)
```

---

### Stage 4: Business Logic (Day 10-12)

#### 7. Use Cases

Business logic layer.

**Key SQLAlchemy patterns:**

1. **SELECT queries:**
```python
result = await db.execute(select(User).where(User.id == user_id))
user = result.scalar_one_or_none()
```

2. **INSERT:**
```python
user = User(email="test@example.com")
db.add(user)
await db.flush()  # Get ID without commit
await db.refresh(user)  # Load data from DB
```

3. **UPDATE:**
```python
user.email = "new@example.com"
await db.flush()
```

4. **DELETE:**
```python
await db.delete(user)
```

**Experiment:**
Add method to search users by name:
```python
async def search_by_name(
    db: AsyncSession,
    query: str
) -> List[User]:
    result = await db.execute(
        select(UserModel).where(UserModel.full_name.ilike(f"%{query}%"))
    )
    return list(result.scalars().all())
```

---

### Stage 5: API Routes (Day 13-15)

#### 8. FastAPI Controllers

HTTP endpoints.

**Key concepts:**

1. **Dependency Injection:**
```python
async def create_user(
    user_data: CreateUserDto,           # Request body (auto-validated)
    db: AsyncSession = Depends(get_db)  # DI
):
```

2. **Response Models:**
```python
@router.post("", response_model=UserResponseDto)
# FastAPI automatically:
# - Validates response
# - Generates OpenAPI schema
# - Filters fields (if needed)
```

3. **HTTP Status Codes:**
```python
@router.post("", status_code=status.HTTP_201_CREATED)
```

4. **Error Handling:**
```python
if not user:
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User not found"
    )
```

**Experiment:**
Add new endpoint for search:
```python
@router.get("/search")
async def search_users(
    q: str = Query(..., min_length=2),
    db: AsyncSession = Depends(get_db)
):
    users = await UserService.search_by_name(db, q)
    return users
```

---

### Stage 6: Relationships (Day 16-18)

#### 9. SQLAlchemy Relationships

Table relationships example.

**Key concepts:**

1. **Foreign Key:**
```python
user_id: Mapped[int] = mapped_column(
    ForeignKey("users.id", ondelete="CASCADE"),
    nullable=False
)
```

2. **Relationship:**
```python
# Eager loading (loaded automatically)
user: Mapped["User"] = relationship("User", lazy="selectin")

# Lazy loading (on demand)
user: Mapped["User"] = relationship("User", lazy="joined")
```

**Experiment:**
```python
# Create post and see how user loads automatically
post = await PostService.get_by_id(db, 1)
print(post.user.email)  # User loaded automatically!
```

---

### Stage 7: Main Application (Day 19-20)

#### 10. `src/main.py`

Application entry point.

**Key concepts:**

1. **Lifespan events:**
```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("Starting up...")
    yield
    # Shutdown
    print("Shutting down...")
```

2. **Middleware:**
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
)
```

3. **Router registration:**
```python
app.include_router(users_router, prefix="/api")
```

---

### Stage 8: Migrations (Day 21-22)

#### 11. Alembic

Database migrations.

**Alembic commands:**
```bash
# Create migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1

# History
alembic history

# Current version
alembic current
```

**Important:**
All models must be imported in `env.py`:
```python
from src.modules.users.infrastructure.persistence.user_model import UserModel
from src.modules.posts.infrastructure.persistence.post_model import PostModel
```

---

### Stage 9: Testing (Day 23-25)

#### 12. `tests/conftest.py`

Pytest fixtures.

**Key fixtures:**
- `db_session` - test database
- `client` - HTTP client for API tests

#### 13. `tests/test_users.py`

API tests.

**Example:**
```python
@pytest.mark.asyncio
async def test_create_user(client: AsyncClient):
    response = await client.post(
        "/api/users",
        json={"email": "test@example.com"}
    )
    assert response.status_code == 201
```

---

## Practice Exercises

### Level 1: Basic Operations
1. Add `bio` field to User model
2. Create migration
3. Update schemas and API
4. Write tests

### Level 2: New Features
1. Create Comments module for posts
2. Add Post -> Comments relationship (OneToMany)
3. Implement CRUD for comments
4. Add filtering by post_id

### Level 3: Advanced
1. Add JWT authentication
2. Create middleware for token validation
3. Add role-based access control
4. Write integration tests

### Level 4: Production-ready
1. Add Redis for caching
2. Implement rate limiting
3. Add logging (structlog)
4. Create Docker setup

---

## Debugging Tips

### 1. SQL Queries
To see all SQL queries:
```python
# src/core/database.py
engine = create_async_engine(
    settings.database_url,
    echo=True  # Enable SQL logging
)
```

### 2. Pydantic validation errors
```python
from pydantic import ValidationError

try:
    user = CreateUserDto(email="invalid")
except ValidationError as e:
    print(e.json())  # Detailed error info
```

### 3. FastAPI debug mode
```python
# .env
DEBUG=True
```

### 4. IPython for experiments
```bash
poetry add ipython --group dev
poetry run ipython

# In IPython:
from src.core.database import AsyncSessionLocal

async with AsyncSessionLocal() as db:
    users = await UserService.get_all(db)
    print(users)
```

---

Good luck learning!
