# Docker Environments

Separate Docker configurations for development and testing environments.

---

## Structure

```
docker/
├── development/          # Development environment
│   ├── docker-compose.yml
│   └── .env.development
└── test/                # Test environment
    ├── docker-compose.yml
    └── .env.test
```

---

## Development Environment

### Services

- **PostgreSQL** (port 5432) - Development database
- **Redis** (port 6379) - Cache and queues
- **pgAdmin** (port 5050) - Web UI for PostgreSQL
- **MailHog** (ports 1025, 8025) - Email testing

### Quick Start

```bash
# Start services
make docker-dev-up

# Setup database (migrations + seeds)
make dev-setup

# Start application
make dev-start

# Documentation: http://localhost:8000/docs
```

### Service Access

- **PostgreSQL**: `postgresql://postgres:postgres@localhost:5432/python_app_dev`
- **Redis**: `redis://localhost:6379/0`
- **pgAdmin**: http://localhost:5050 (admin@admin.com / admin)
- **MailHog UI**: http://localhost:8025

### Commands

```bash
make docker-dev-up        # Start dev services
make docker-dev-down      # Stop dev services
make docker-dev-logs      # View logs
make docker-dev-clean     # Remove volumes and data

make dev-migrate          # Apply migrations
make dev-migration        # Create migration (message='...')
make dev-seed             # Seed database
make dev-setup            # Migrations + seeds
make dev-start            # Start FastAPI app
```

---

## Test Environment

### Services

- **PostgreSQL** (port 5433) - Test database
- **Redis** (port 6380) - Test cache (no persistence)
- **MinIO** (ports 9000, 9001) - S3-compatible storage

### Quick Start

```bash
# Start test services
make docker-test-up

# Setup test database
make test-setup

# Run tests
make test-run
```

### Service Access

- **PostgreSQL**: `postgresql://test_user:test_password@localhost:5433/python_app_test`
- **Redis**: `redis://localhost:6380/0`
- **MinIO UI**: http://localhost:9001 (minioadmin / minioadmin)
- **MinIO API**: http://localhost:9000

### Commands

```bash
make docker-test-up       # Start test services
make docker-test-down     # Stop test services
make docker-test-logs     # View logs
make docker-test-clean    # Remove volumes and data

make test-migrate         # Apply migrations to test DB
make test-seed            # Seed test database
make test-setup           # Migrations + seeds
make test-run             # Run tests
make test-cov             # Run tests with coverage
```

---

## Database Migrations & Seeds

### Development

```bash
# Create migration (after model changes)
make dev-migration message="initial migration"

# Apply migrations
make dev-migrate

# Seed database with test data
make dev-seed

# Quick setup (migrations + seeds)
make dev-setup

# Rollback last migration
make dev-migrate-down
```

### Test Data

Seeds create:
- **5 users**: admin, john, jane, bob, alice (1 inactive)
- **10 posts**: 9 published, 1 draft

Test emails:
- admin@example.com
- john.doe@example.com
- jane.smith@example.com
- bob.wilson@example.com
- alice.brown@example.com (inactive)

---

## Troubleshooting

### Ports Already in Use

Edit ports in `docker-compose.yml`:

```yaml
ports:
  - "NEW_PORT:CONTAINER_PORT"
```

### Database Connection Issues

Check container status:

```bash
docker compose ps
docker compose logs postgres
```

### Clean Everything

```bash
# From project root
make docker-clean

# Or manually
cd docker/development
docker compose down -v --remove-orphans

cd ../test
docker compose down -v --remove-orphans

# Remove all unused volumes
docker volume prune
```

---

## Environment Configuration

The `make docker-dev-up` and `make docker-test-up` commands automatically copy the appropriate `.env` file to the project root.

Manual setup (if needed):

```bash
# Development
cp docker/development/.env.development .env

# Test
cp docker/test/.env.test .env
```
