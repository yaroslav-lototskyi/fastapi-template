# Makefile for convenient project management
# Similar to npm scripts in package.json

.PHONY: install clean format lint help \
	dev-start dev-migrate dev-migration dev-seed dev-setup \
	test-run test-cov test-migrate test-seed test-setup \
	docker-dev-up docker-dev-down docker-dev-logs docker-dev-clean \
	docker-test-up docker-test-down docker-test-logs docker-test-clean \
	docker-up docker-down docker-clean

# ==================== General ====================

# Install dependencies
install:
	poetry install

# ==================== Development Environment ====================

# Start application with hot reload
dev-start:
	poetry run uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

# Apply migrations (development)
dev-migrate:
	poetry run alembic upgrade head

# Create new migration
dev-migration:
	poetry run alembic revision --autogenerate -m "$(message)"

# Rollback migration
dev-migrate-down:
	poetry run alembic downgrade -1

# Seed dev database with test data
dev-seed:
	poetry run python scripts/seed.py

# Full dev database setup (migrations + seeds)
dev-setup: dev-migrate dev-seed
	@echo "✅ Development database ready!"
	@echo "Start app with: make dev-start"

# ==================== Test Environment ====================

# Run tests
test-run:
	poetry run pytest

# Run tests with coverage
test-cov:
	poetry run pytest --cov=src --cov-report=html

# Apply migrations (test database)
test-migrate:
	poetry run alembic upgrade head

# Seed test database with data
test-seed:
	poetry run python scripts/seed.py

# Full test database setup (migrations + seeds)
test-setup: test-migrate test-seed
	@echo "✅ Test database ready!"
	@echo "Run tests with: make test-run"

# ==================== Code Quality ====================

# Format code
format:
	python3 -m black src tests
	python3 -m ruff check --fix src tests

# Check code quality
lint:
	python3 -m black --check src tests
	python3 -m ruff check src tests
	python3 -m mypy src

# Clean cache and temporary files
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	rm -f test.db

# ==================== Docker Commands ====================

# Development environment
docker-dev-up:
	@echo "🚀 Starting development services..."
	@cp docker/development/.env.development .env
	@cd docker/development && docker compose up -d
	@echo ""
	@echo "✅ Development services are running!"
	@echo ""
	@echo "📊 Services:"
	@echo "  • PostgreSQL: postgresql://postgres:postgres@localhost:5432/python_app_dev"
	@echo "  • Redis:      redis://localhost:6379"
	@echo "  • pgAdmin:    http://localhost:5050 (admin@admin.com / admin)"
	@echo "  • MailHog:    http://localhost:8025"
	@echo ""
	@echo "Next steps:"
	@echo "  1. make dev-setup    (run migrations + seed data)"
	@echo "  2. make dev-start    (start FastAPI app)"

docker-dev-down:
	cd docker/development && docker compose down

docker-dev-logs:
	cd docker/development && docker compose logs -f

docker-dev-clean:
	cd docker/development && docker compose down -v --remove-orphans

# Test environment
docker-test-up:
	@echo "🧪 Starting test services..."
	@cp docker/test/.env.test .env
	@cd docker/test && docker compose up -d
	@echo ""
	@echo "✅ Test services are running!"
	@echo ""
	@echo "📊 Services:"
	@echo "  • PostgreSQL: postgresql://test_user:test_password@localhost:5433/python_app_test"
	@echo "  • Redis:      redis://localhost:6380"
	@echo "  • MinIO:      http://localhost:9001 (minioadmin / minioadmin)"
	@echo ""
	@echo "Next steps:"
	@echo "  1. make test-setup   (prepare test database)"
	@echo "  2. make test-run     (run tests)"

docker-test-down:
	cd docker/test && docker compose down

docker-test-logs:
	cd docker/test && docker compose logs -f

docker-test-clean:
	cd docker/test && docker compose down -v --remove-orphans

# Both environments
docker-up: docker-dev-up docker-test-up
	@echo "All Docker services started"

docker-down: docker-dev-down docker-test-down
	@echo "All Docker services stopped"

docker-clean: docker-dev-clean docker-test-clean
	@echo "All Docker data cleaned"

# ==================== Help ====================

# Show help
help:
	@echo "╔════════════════════════════════════════════════════════════╗"
	@echo "║           FastAPI Application - Makefile Commands         ║"
	@echo "╚════════════════════════════════════════════════════════════╝"
	@echo ""
	@echo "📦 General:"
	@echo "  make install           - Install dependencies"
	@echo "  make clean             - Clean temporary files"
	@echo "  make format            - Format code"
	@echo "  make lint              - Check code quality"
	@echo ""
	@echo "🔧 Development Environment:"
	@echo "  make docker-dev-up     - Start Docker services (PostgreSQL, Redis, etc.)"
	@echo "  make dev-migration     - Create new migration (message='...')"
	@echo "  make dev-setup         - Apply migrations + seed database"
	@echo "  make dev-start         - Start application with hot reload"
	@echo ""
	@echo "  Individual commands:"
	@echo "    make dev-migrate     - Only apply migrations"
	@echo "    make dev-seed        - Only seed database"
	@echo "    make dev-migrate-down - Rollback migration"
	@echo ""
	@echo "🧪 Test Environment:"
	@echo "  make docker-test-up    - Start test Docker services"
	@echo "  make test-setup        - Prepare test database (migrations + seeds)"
	@echo "  make test-run          - Run tests"
	@echo "  make test-cov          - Run tests with coverage"
	@echo ""
	@echo "  Individual commands:"
	@echo "    make test-migrate    - Apply migrations to test database"
	@echo "    make test-seed       - Seed test database"
	@echo ""
	@echo "🐳 Docker Management:"
	@echo "  Dev:"
	@echo "    make docker-dev-down   - Stop dev services"
	@echo "    make docker-dev-logs   - View dev logs"
	@echo "    make docker-dev-clean  - Clean dev data"
	@echo ""
	@echo "  Test:"
	@echo "    make docker-test-down  - Stop test services"
	@echo "    make docker-test-logs  - View test logs"
	@echo "    make docker-test-clean - Clean test data"
	@echo ""
	@echo "  All:"
	@echo "    make docker-up         - Start all environments"
	@echo "    make docker-down       - Stop all environments"
	@echo "    make docker-clean      - Clean all data"
	@echo ""
	@echo "🚀 Quick Start:"
	@echo "  1. make docker-dev-up"
	@echo "  2. make dev-setup"
	@echo "  3. make dev-start"
	@echo ""
	@echo "📚 Docs: http://localhost:8000/docs (after starting)"
