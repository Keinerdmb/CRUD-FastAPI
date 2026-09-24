from fastapi.testclient import TestClient


def test_root_endpoint(client: TestClient):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_product(client: TestClient):
    payload = {
        "name": "Teclado Mecanico",
        "description": "Teclado RGB switch blue",
        "price": 49.99,
        "stock": 10,
    }
    response = client.post("/products/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["id"] is not None
    assert data["name"] == payload["name"]
    assert data["price"] == payload["price"]
    assert data["stock"] == payload["stock"]


def test_create_product_duplicate_name(client: TestClient):
    payload = {
        "name": "Mouse Gamer",
        "price": 25.0,
        "stock": 5,
    }
    first_resp = client.post("/products/", json=payload)
    assert first_resp.status_code == 201

    second_resp = client.post("/products/", json=payload)
    assert second_resp.status_code == 409


def test_create_product_validation_error_price_and_stock(client: TestClient):
    # Precio <= 0 debe fallar por validacion de Pydantic (422)
    response = client.post(
        "/products/",
        json={"name": "Monitor", "price": -10.0, "stock": 5},
    )
    assert response.status_code == 422

    # Stock < 0 debe fallar por validacion de Pydantic (422)
    response = client.post(
        "/products/",
        json={"name": "Monitor", "price": 100.0, "stock": -1},
    )
    assert response.status_code == 422


def test_list_products_and_pagination(client: TestClient):
    for i in range(5):
        client.post(
            "/products/",
            json={"name": f"Item {i}", "price": 10.0 + i, "stock": i},
        )

    response = client.get("/products/?skip=1&limit=2")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["name"] == "Item 1"
    assert data[1]["name"] == "Item 2"


def test_get_product_by_id(client: TestClient):
    create_resp = client.post(
        "/products/",
        json={"name": "Audifonos", "price": 30.0, "stock": 3},
    )
    product_id = create_resp.json()["id"]

    response = client.get(f"/products/{product_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Audifonos"


def test_get_product_not_found(client: TestClient):
    response = client.get("/products/99999")
    assert response.status_code == 404


def test_update_product(client: TestClient):
    create_resp = client.post(
        "/products/",
        json={"name": "Webcam", "price": 40.0, "stock": 8},
    )
    product_id = create_resp.json()["id"]

    update_resp = client.put(
        f"/products/{product_id}",
        json={"price": 35.0, "stock": 12},
    )
    assert update_resp.status_code == 200
    updated = update_resp.json()
    assert updated["price"] == 35.0
    assert updated["stock"] == 12
    assert updated["name"] == "Webcam"


def test_update_product_duplicate_name(client: TestClient):
    client.post("/products/", json={"name": "Laptop", "price": 1000.0, "stock": 2})
    p2 = client.post("/products/", json={"name": "Tablet", "price": 500.0, "stock": 4}).json()

    # Intentar cambiar Tablet a Laptop
    update_resp = client.put(f"/products/{p2['id']}", json={"name": "Laptop"})
    assert update_resp.status_code == 409


def test_delete_product(client: TestClient):
    create_resp = client.post(
        "/products/",
        json={"name": "Cable HDMI", "price": 5.0, "stock": 20},
    )
    product_id = create_resp.json()["id"]

    delete_resp = client.delete(f"/products/{product_id}")
    assert delete_resp.status_code == 204

    get_resp = client.get(f"/products/{product_id}")
    assert get_resp.status_code == 404
