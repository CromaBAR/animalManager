# Program to test the animal API
from fastapi.testclient import TestClient
from Backend.api.db.models.animal import Animal
from gestorAnimales.main import app

client = TestClient(app)

# Test the get_animals function
def test_get_animals():
    response = client.get("/animals/")
    assert response.status_code == 200
    assert response.json() == list(Animal)
    