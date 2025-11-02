"""
Database seeding script.
Створює тестові дані для development середовища.
"""
import asyncio
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from sqlalchemy import select
from src.core.database import AsyncSessionLocal
from src.modules.users.infrastructure.persistence.user_model import UserModel
from src.modules.posts.infrastructure.persistence.post_model import PostModel

async def seed_users():
    """Створення тестових користувачів"""
    print("👤 Seeding users...")

    users_data = [
        {
            "email": "admin@example.com",
            "username": "admin",
            "full_name": "Admin User",
            "is_active": True,
        },
        {
            "email": "john.doe@example.com",
            "username": "johndoe",
            "full_name": "John Doe",
            "is_active": True,
        },
        {
            "email": "jane.smith@example.com",
            "username": "janesmith",
            "full_name": "Jane Smith",
            "is_active": True,
        },
        {
            "email": "bob.wilson@example.com",
            "username": "bobwilson",
            "full_name": "Bob Wilson",
            "is_active": True,
        },
        {
            "email": "alice.brown@example.com",
            "username": "alicebrown",
            "full_name": "Alice Brown",
            "is_active": False,  # Inactive user for testing
        },
    ]

    async with AsyncSessionLocal() as session:
        users = [UserModel(**user_data) for user_data in users_data]
        session.add_all(users)
        await session.commit()

        print(f"✓ Created {len(users)} users")
        return users


async def seed_posts(users):
    """Створення тестових постів"""
    print("📝 Seeding posts...")

    posts_data = [
        {
            "title": "Welcome to FastAPI",
            "content": "This is a comprehensive guide to building modern web applications with FastAPI. FastAPI is a modern, fast (high-performance), web framework for building APIs with Python 3.7+ based on standard Python type hints.",
            "is_published": True,
            "user_id": users[0].id,  # admin
        },
        {
            "title": "Getting Started with Clean Architecture",
            "content": "Clean Architecture is a software design philosophy that separates the elements of a design into ring levels. An important goal of Clean Architecture is to provide developers with a way to organize code in such a way that it encapsulates the business logic but keeps it separate from the delivery mechanism.",
            "is_published": True,
            "user_id": users[0].id,  # admin
        },
        {
            "title": "Understanding Dependency Injection",
            "content": "Dependency Injection is a design pattern used to implement IoC (Inversion of Control). It allows the creation of dependent objects outside of a class and provides those objects to a class through different ways.",
            "is_published": True,
            "user_id": users[1].id,  # john
        },
        {
            "title": "Python Async/Await Tutorial",
            "content": "Asynchronous programming is a programming paradigm that allows you to write concurrent code that runs in a single thread. In Python, we use async/await syntax to write asynchronous code.",
            "is_published": True,
            "user_id": users[1].id,  # john
        },
        {
            "title": "SQLAlchemy 2.0 Best Practices",
            "content": "SQLAlchemy 2.0 brings many improvements and new features. This post covers the best practices for using SQLAlchemy 2.0 in modern Python applications.",
            "is_published": True,
            "user_id": users[2].id,  # jane
        },
        {
            "title": "Docker for Python Developers",
            "content": "Docker has become an essential tool for modern software development. Learn how to containerize your Python applications and manage multiple environments.",
            "is_published": True,
            "user_id": users[2].id,  # jane
        },
        {
            "title": "Testing FastAPI Applications",
            "content": "Testing is crucial for maintaining high-quality code. This guide shows you how to write effective tests for your FastAPI applications using pytest.",
            "is_published": True,
            "user_id": users[3].id,  # bob
        },
        {
            "title": "Draft: Advanced PostgreSQL Features",
            "content": "This is a draft post exploring advanced PostgreSQL features like JSONB, full-text search, and advanced indexing strategies.",
            "is_published": False,  # Draft post
            "user_id": users[3].id,  # bob
        },
        {
            "title": "API Design Best Practices",
            "content": "Designing a good API is an art. This post covers REST API design best practices including proper use of HTTP methods, status codes, and resource naming.",
            "is_published": True,
            "user_id": users[1].id,  # john
        },
        {
            "title": "Poetry: Modern Python Dependency Management",
            "content": "Poetry is a tool for dependency management and packaging in Python. It allows you to declare the libraries your project depends on and it will manage them for you.",
            "is_published": True,
            "user_id": users[2].id,  # jane
        },
    ]

    async with AsyncSessionLocal() as session:
        posts = [PostModel(**post_data) for post_data in posts_data]
        session.add_all(posts)
        await session.commit()

        print(f"✓ Created {len(posts)} posts")


async def main():
    """Головна функція для запуску seeds"""
    print("🌱 Starting database seeding...\n")

    try:
        # Очищення даних (опціонально)
        # await clear_data()

        # Створення користувачів
        users = await seed_users()

        # Створення постів
        await seed_posts(users)

        print("\n✅ Database seeding completed successfully!")
        print("\n📊 Summary:")
        print(f"   • Users: 5 (4 active, 1 inactive)")
        print(f"   • Posts: 10 (9 published, 1 draft)")
        print("\n🔐 Test credentials:")
        print("   • admin@example.com")
        print("   • john.doe@example.com")
        print("   • jane.smith@example.com")
        print("   • bob.wilson@example.com")

    except Exception as e:
        print(f"\n❌ Error during seeding: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(main())
