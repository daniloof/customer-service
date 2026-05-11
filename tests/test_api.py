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
    assert response.status_code == 201

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

    assert first_response.status_code == 201

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

    assert customer_response.status_code == 201, customer_response.json()

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

    assert response.status_code == 201, response.json()

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

def test_get_customer_invalid_uuid():
    response = client.get("/customers/id-inexistente")
    assert response.status_code == 422  # ← UUID inválido, rejeitado pelo Pydantic

def test_get_customer_not_found():
    response = client.get("/customers/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404  # ← UUID válido mas não existe no banco

def test_list_customers_empty():
    response = client.get("/customers")
    assert response.status_code == 200
    assert response.json() == []

def test_list_addresses_by_customer():
    # cria cliente
    customer = client.post("/customers", json={"name": "John", "email": "john@example.com"}).json()
    # adiciona endereço
    client.post(f"/customers/{customer['id']}/addresses", json={
        "street": "Rua A", "city": "SP", "state": "SP", "zip_code": "09000000"
    })
    # lista endereços via GET /customers/{id}
    response = client.get(f"/customers/{customer['id']}")
    assert response.status_code == 200
    assert len(response.json()["addresses"]) == 1

def test_update_customer():
    # cria
    response = client.post("/customers", json={"name": "John", "email": "john@example.com"})
    customer_id = response.json()["id"]

    # atualiza
    response = client.put(f"/customers/{customer_id}", json={
        "name": "John Updated",
        "email": "john.updated@example.com"
    })
    assert response.status_code == 200
    assert response.json()["name"] == "John Updated"
    assert response.json()["email"] == "john.updated@example.com"

def test_update_customer_not_found():
    response = client.put(
        "/customers/00000000-0000-0000-0000-000000000000",
        json={"name": "John", "email": "john@example.com"}
    )
    assert response.status_code == 404

def test_update_customer_duplicate_email():
    client.post("/customers", json={"name": "John", "email": "john@example.com"})
    jane = client.post("/customers", json={"name": "Jane", "email": "jane@example.com"})
    jane_id = jane.json()["id"]

    response = client.put(f"/customers/{jane_id}", json={
        "name": "Jane",
        "email": "john@example.com"  # email já existe
    })
    assert response.status_code == 409

def test_delete_customer():
    response = client.post("/customers", json={"name": "John", "email": "john@example.com"})
    customer_id = response.json()["id"]

    response = client.delete(f"/customers/{customer_id}")
    assert response.status_code == 204

    # confirma que foi deletado
    response = client.get(f"/customers/{customer_id}")
    assert response.status_code == 404

def test_delete_customer_not_found():
    response = client.delete("/customers/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404

def test_delete_address():
    # cria cliente
    customer = client.post("/customers", json={"name": "John", "email": "john@example.com"}).json()
    customer_id = customer["id"]

    # adiciona endereço
    address = client.post(f"/customers/{customer_id}/addresses", json={
        "street": "Rua A", "city": "SP", "state": "SP", "zip_code": "09000000"
    }).json()
    address_id = address["id"]

    # deleta endereço
    response = client.delete(f"/customers/{customer_id}/addresses/{address_id}")
    assert response.status_code == 204

    # confirma que foi deletado
    response = client.get(f"/customers/{customer_id}")
    assert response.status_code == 200
    assert len(response.json()["addresses"]) == 0

def test_delete_address_customer_not_found():
    response = client.delete(
        "/customers/00000000-0000-0000-0000-000000000000/addresses/00000000-0000-0000-0000-000000000001"
    )
    assert response.status_code == 404    