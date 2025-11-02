# Database Seeding

Script to populate the database with test data.

---

## seed.py

Populates the database with test data for development and testing.

### Usage

```bash
# Via Makefile (recommended)
make dev-seed

# Or directly
poetry run python scripts/seed.py
```

### Test Data Created

**Users (5):**
- admin@example.com (admin) - active
- john.doe@example.com (johndoe) - active
- jane.smith@example.com (janesmith) - active
- bob.wilson@example.com (bobwilson) - active
- alice.brown@example.com (alicebrown) - **inactive**

**Posts (10):**
- 9 published posts from various users
- 1 draft (is_published=False)

---

## Quick Workflow

```bash
# 1. Start Docker services
make docker-dev-up

# 2. Setup database (migrations + seeds)
make dev-setup

# 3. Start application
make dev-start
```

---

## Customization

To add custom test data, modify the `users_data` and `posts_data` arrays in `seed.py`.

To clear existing data before seeding, uncomment the line:

```python
# await clear_data()  # Uncomment to clear data before seeding
```
