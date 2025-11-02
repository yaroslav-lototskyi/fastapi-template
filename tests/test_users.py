"""
User endpoints tests.

Integration tests for user API endpoints using pytest and httpx.
"""
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_user(client: AsyncClient):
    """Test creating a new user."""
    response = await client.post(
        "/api/users/",
        json={
            "email": "test@example.com",
            "username": "testuser",
            "full_name": "Test User",
        },
    )

    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["username"] == "testuser"
    assert data["full_name"] == "Test User"
    assert "id" in data
    assert "created_at" in data


@pytest.mark.asyncio
async def test_create_user_duplicate_email(client: AsyncClient):
    """Test creating user with duplicate email."""
    user_data = {
        "email": "test@example.com",
        "username": "testuser",
    }

    # Create first user
    response1 = await client.post("/api/users/", json=user_data)
    assert response1.status_code == 201

    # Try to create second user with same email
    user_data["username"] = "different"
    response2 = await client.post("/api/users/", json=user_data)
    assert response2.status_code == 400
    assert "Email already registered" in response2.json()["detail"]


@pytest.mark.asyncio
async def test_get_users(client: AsyncClient):
    """Test getting list of users."""
    # Create some users
    for i in range(3):
        await client.post(
            "/api/users/",
            json={
                "email": f"user{i}@example.com",
                "username": f"user{i}",
            },
        )

    # Get users list
    response = await client.get("/api/users/")
    assert response.status_code == 200

    data = response.json()
    assert data["total"] == 3
    assert len(data["items"]) == 3
    assert data["page"] == 1
    assert data["page_size"] == 10


@pytest.mark.asyncio
async def test_get_user_by_id(client: AsyncClient):
    """Test getting user by ID."""
    # Create user
    create_response = await client.post(
        "/api/users/",
        json={
            "email": "test@example.com",
            "username": "testuser",
        },
    )
    user_id = create_response.json()["id"]

    # Get user by ID
    response = await client.get(f"/api/users/{user_id}")
    assert response.status_code == 200

    data = response.json()
    assert data["id"] == user_id
    assert data["email"] == "test@example.com"


@pytest.mark.asyncio
async def test_get_user_not_found(client: AsyncClient):
    """Test getting non-existent user."""
    response = await client.get("/api/users/999")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_update_user(client: AsyncClient):
    """Test updating user."""
    # Create user
    create_response = await client.post(
        "/api/users/",
        json={
            "email": "test@example.com",
            "username": "testuser",
        },
    )
    user_id = create_response.json()["id"]

    # Update user
    response = await client.patch(
        f"/api/users/{user_id}",
        json={"full_name": "Updated Name"},
    )
    assert response.status_code == 200

    data = response.json()
    assert data["full_name"] == "Updated Name"
    assert data["email"] == "test@example.com"  # Unchanged


@pytest.mark.asyncio
async def test_delete_user(client: AsyncClient):
    """Test deleting user."""
    # Create user
    create_response = await client.post(
        "/api/users/",
        json={
            "email": "test@example.com",
            "username": "testuser",
        },
    )
    user_id = create_response.json()["id"]

    # Delete user
    response = await client.delete(f"/api/users/{user_id}")
    assert response.status_code == 204

    # Verify user is deleted
    get_response = await client.get(f"/api/users/{user_id}")
    assert get_response.status_code == 404
