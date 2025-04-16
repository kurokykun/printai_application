import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# Prueba para el endpoint /init
def test_init_scraping():
    response = client.post("/init")
    assert response.status_code == 200
    assert "message" in response.json()

# Prueba para el endpoint /books/search
def test_search_books():
    response = client.post("/books/search", json={"title": "ni"})
    assert response.status_code == 200
    assert isinstance(response.json(), list)

# Prueba para el endpoint /headlines
def test_get_headlines():
    response = client.get("/headlines")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
