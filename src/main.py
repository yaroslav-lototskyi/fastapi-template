"""
Main FastAPI application with Clean Architecture + Hybrid DI.

Combines:
- Clean Architecture (DDD, SOLID)
- Hybrid DI (dependency-injector + FastAPI Depends)
- Structured logging (structlog)

Application entry point and configuration.
"""
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.core.config import get_settings
from src.core.infrastructure.container import ApplicationContainer
from src.modules.users.presentation import router as users_router
from src.modules.posts.presentation import router as posts_router

settings = get_settings()

# ==========================================
# Initialize DI Container (Singleton services)
# ==========================================

container = ApplicationContainer()

# Configure container with settings
container.config.app_env.from_value(settings.app_env)
container.config.smtp_host.from_value("smtp.gmail.com")
container.config.smtp_port.from_value(587)
container.config.sms_api_key.from_value("SECRET_KEY_123")


# ==========================================
# Application Lifespan
# ==========================================


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan events.

    Handles startup and shutdown operations:
    - Startup: Initialize services, wire DI container, logging
    - Shutdown: Cleanup resources, unwire DI container
    """
    # Startup
    logger = container.logger()
    logger.info(
        "Application starting",
        env=settings.app_env,
        version="1.0.0",
        architecture="Clean Architecture + Hybrid DI",
    )

    # Wire container for automatic dependency injection
    # This enables @inject decorator to work
    container.wire(
        modules=[
            "src.core.infrastructure.container",
        ]
    )

    logger.info("DI Container wired", services=["Logger", "Email", "SMS", "Notification"])

    yield

    # Shutdown
    logger.info("Application shutting down")
    container.unwire()


# ==========================================
# Create FastAPI Application
# ==========================================

app = FastAPI(
    title="Python FastAPI - Clean Architecture + Hybrid DI",
    description="Modern Python backend with Clean Architecture, DDD, SOLID, and Hybrid DI pattern",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Attach container to app (for access in tests/middleware if needed)
app.container = container


# ==========================================
# Health Check
# ==========================================


@app.get("/health", tags=["health"], response_model=None)
async def health_check():
    """
    Health check endpoint.

    Returns application status and architecture info.
    """
    return {
        "status": "healthy",
        "environment": settings.app_env,
        "architecture": "Clean Architecture + DDD + Hybrid DI",
        "di_pattern": "dependency-injector (Singleton) + FastAPI Depends (per-request)",
        "logging": "structlog (structured)",
    }


# ==========================================
# Register Module Routers
# ==========================================

# Register feature module routers
app.include_router(users_router, prefix="/api")
app.include_router(posts_router, prefix="/api")


# ==========================================
# Run Application
# ==========================================

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "src.main:app",
        host=settings.app_host,
        port=settings.app_port,
        reload=settings.debug,
    )
