from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_user():
    response = client.post("/user/new/", json={
        "username": "mmuster",
        "firstName": "Max",
        "lastName": "Muster",
        "password": "Secure_Pass",
        "email": "max-muster@exemple.de",
    })
    #assert response.status_code == 201
    returned_user = response.json()
    assert returned_user["username"] == "mmuster"
    assert returned_user["email"] == "max-muster@exemple.de"


# starte with: pytest user_test.py