from fastapi.testclient import TestClient
from src.main import app
from src.infrastructure.db.dependencies import get_db
from tests.test_database import TestingSessionLocal
from uuid import uuid4

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_create_customer_api():
    unique_email = f"{uuid4()}@example.com"
    response = client.post("/customers/", json={"name": "John Doe", "email": unique_email})
    assert response.status_code == 200

    data = response.json()
    assert data["name"] == "John Doe"
    assert data["email"] == unique_email
    assert "id" in data

def test_create_customer_duplicate_email():
    email = f"duplicate_{uuid4()}@example.com"

    first_response = client.post(
        "/customers/",
        json={
            "name": "John Doe",
            "email": email
        }
    )

    assert first_response.status_code == 200

    second_response = client.post(
        "/customers/",
        json={
            "name": "Jane Doe",
            "email": email
        }
    )

    assert second_response.status_code == 409

    data = second_response.json()

    assert "detail" in data
    assert "Email already exists" in data["detail"]

def test_add_address_api():
    unique_email = f"address_{uuid4()}@example.com"

    customer_response = client.post(
        "/customers/",
        json={
            "name": "John Doe",
            "email": unique_email
        }
    )

    assert customer_response.status_code == 200, customer_response.json()

    customer_id = customer_response.json()["id"]

    response = client.post(
        f"/customers/{customer_id}/addresses",
        json={
            "street": "Rua A",
            "city": "São Paulo",
            "state": "SP",
            "zip_code": "09000-000"
        }
    )

    assert response.status_code == 200, response.json()

    data = response.json()

    assert data["customer_id"] == customer_id
    assert data["street"] == "Rua A"
    assert data["city"] == "São Paulo"
    assert data["state"] == "SP"
    assert data["zip_code"] == "09000-000"

def test_add_address_nonexistent_customer():
    fake_id = str(uuid4())

    response = client.post(
        f"/customers/{fake_id}/addresses",
        json={
            "street": "Rua A",
            "city": "São Paulo",
            "state": "SP",
            "zip_code": "09000-000"
        }
    )

    assert response.status_code == 404

    data = response.json()

    assert "detail" in data
    assert "Customer not found" in data["detail"]

def test_add_address_invalid_zip():
    unique_email = f"zip_{uuid4()}@example.com"

    customer_response = client.post(
        "/customers/",
        json={
            "name": "John Doe",
            "email": unique_email
        }
    )

    customer_id = customer_response.json()["id"]

    response = client.post(
        f"/customers/{customer_id}/addresses",
        json={
            "street": "Rua A",
            "city": "São Paulo",
            "state": "SP",
            "zip_code": "123"
        }
    )

    assert response.status_code == 400

    data = response.json()

    assert "detail" in data