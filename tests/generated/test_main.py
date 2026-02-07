"""Tests for main module."""

import sys
import os
import pytest
from datetime import datetime
from fastapi.testclient import TestClient
from main import app

sys.path.insert(0, r"/home/runner/work/Fastapi_application/Fastapi_application/pipeline/target_repo")
def client():
    return TestClient(app)

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def setup_empty_items(monkeypatch):
    # Mock the items_db to be empty for this test
    monkeypatch.setattr("main.items_db", [])


class TestMainUnit:
    """Unit tests for main."""

    def test_root_response(self, client):
        """UNIVERSAL test for maximum coverage."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert data["message"] == "Welcome to Sample FastAPI Application"
        assert "version" in data
        assert "docs" in data
        assert "redoc" in data

    def test_health_check_response(self, client):
        """UNIVERSAL test for maximum coverage."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data and data["status"] == "healthy"
        assert "timestamp" in data

    def test_create_item_success(self, client):
        """UNIVERSAL test for maximum coverage."""
        payload = {"name": "Item A", "description": "A test item", "price": 10.5, "quantity": 5}
        response = client.post("/items/", json=payload)
        assert response.status_code == 201
        data = response.json()
        assert data["id"] is not None
        assert data["name"] == payload["name"]
        assert data["price"] == payload["price"]
        assert "created_at" in data
        assert "updated_at" in data

    def test_create_item_missing_fields(self, client):
        """UNIVERSAL test for maximum coverage."""
        payload = {"name": "Item B", "price": 10.5}
        response = client.post("/items/", json=payload)
        assert response.status_code == 422

    def test_create_item_invalid_price(self, client):
        """UNIVERSAL test for maximum coverage."""
        payload = {"name": "Item C", "description": "Invalid price", "price": -5, "quantity": 2}
        response = client.post("/items/", json=payload)
        assert response.status_code == 422

    def test_get_items_empty(self, client, setup_empty_items):
        """Test get_items endpoint when there are no items."""
        response = client.get('/items/')
        assert response.status_code == 200
        assert response.json() == []

    @pytest.mark.parametrize("item_data", [
        ({"name": "Item 1", "description": "Desc 1", "price": 20.0, "quantity": 5}),
        ({"name": "Item 2", "description": "Desc 2", "price": 15.0, "quantity": 10})
    ])
    def test_get_items_with_data(self, client, item_data):
        """UNIVERSAL test for maximum coverage."""
        client.post("/items/", json=item_data)
        response = client.get("/items/")
        assert response.status_code == 200
        data = response.json()
        assert len(data) > 0
        assert isinstance(data, list)

    def test_get_items_pagination(self, client):
        """UNIVERSAL test for maximum coverage."""
        items = []
        for i in range(15):
            item = {"name": f"Item {i}", "description": f"Description {i}", "price": 10.0 * (i + 1), "quantity": i + 10}
            items.append(item)
            client.post("/items/", json=item)

        response = client.get("/items/?skip=5&limit=5")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 5
        assert data[0]["name"] == "Item 5"

    def test_get_item_success(self, client):
        """UNIVERSAL test for maximum coverage."""
        payload = {"name": "Test Item", "description": "A single item", "price": 9.99, "quantity": 1}
        create_response = client.post("/items/", json=payload)
        item_id = create_response.json()["id"]

        response = client.get(f"/items/{item_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == item_id
        assert data["name"] == payload["name"]

    def test_get_item_not_found(self, client):
        """UNIVERSAL test for maximum coverage."""
        response = client.get("/items/99999")
        assert response.status_code == 404

    def test_update_item_success(self, client):
        """UNIVERSAL test for maximum coverage."""
        payload = {"name": "Item To Update", "description": "Update me", "price": 20.0, "quantity": 2}
        create_response = client.post("/items/", json=payload)
        item_id = create_response.json()["id"]
        update_payload = {"name": "Updated Item", "description": "Updated description", "price": 30.0, "quantity": 5}

        response = client.put(f"/items/{item_id}", json=update_payload)
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == update_payload["name"]
        assert data["price"] == update_payload["price"]

    def test_update_item_not_found(self, client):
        """UNIVERSAL test for maximum coverage."""
        update_payload = {"name": "Non-existent Item", "description": "Does not exist", "price": 30.0, "quantity": 5}
        response = client.put("/items/99999", json=update_payload)
        assert response.status_code == 404

    def test_delete_item_success(self, client):
        """UNIVERSAL test for maximum coverage."""
        payload = {"name": "Item To Delete", "description": "Please delete me", "price": 100.0, "quantity": 1}
        create_response = client.post("/items/", json=payload)
        item_id = create_response.json()["id"]

        response = client.delete(f"/items/{item_id}")
        assert response.status_code == 204
        assert response.text == ""

        # Ensure the item is deleted
        get_response = client.get(f"/items/{item_id}")
        assert get_response.status_code == 404

    def test_delete_item_not_found(self, client):
        """UNIVERSAL test for maximum coverage."""
        response = client.delete("/items/99999")
        assert response.status_code == 404

    def test_create_user_success(self, client):
        """UNIVERSAL test for maximum coverage."""
        payload = {"username": "johndoe", "email": "johndoe@email.com", "full_name": "John Doe", "password": "testpass123"}
        response = client.post("/users/", json=payload)
        assert response.status_code == 201
        data = response.json()
        assert data["username"] == payload["username"]
        assert data["email"] == payload["email"]
        assert data["is_active"] is True
        assert "id" in data

    def test_create_user_duplicate_username(self, client):
        """UNIVERSAL test for maximum coverage."""
        payload = {"username": "duplicate", "email": "duplicate@email.com", "full_name": "Duplicate User", "password": "password123"}
        client.post("/users/", json=payload)
        response = client.post("/users/", json=payload)
        assert response.status_code == 400

    def test_get_users(self, client):
        """UNIVERSAL test for maximum coverage."""
        response = client.get("/users/")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    def test_get_user_success(self, client):
        """UNIVERSAL test for maximum coverage."""
        payload = {"username": "janedoe", "email": "janedoe@email.com", "full_name": "Jane Doe", "password": "secure123"}
        create_response = client.post("/users/", json=payload)
        user_id = create_response.json()["id"]

        response = client.get(f"/users/{user_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == user_id

    def test_get_user_not_found(self, client):
        """UNIVERSAL test for maximum coverage."""
        response = client.get("/users/99999")
        assert response.status_code == 404

