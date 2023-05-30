from datetime import datetime

from fastapi.testclient import TestClient
from main import app, authenticate_user

client = TestClient(app)

def test_authenticate_user():
 assert authenticate_user("user1", "password1") == {"username": "user1", "password": "password1", "salary": 1000.0, "next_raise": datetime(2023, 6, 1)}
 assert authenticate_user("user2", "password2") == {"username": "user2", "password": "password2", "salary": 2000.0, "next_raise": datetime(2023, 7, 1)}
 assert authenticate_user("user3", "password3") == False

def test_login():
 response = client.post("/token", data={"username": "user1", "password": "password1"})
 assert response.status_code == 200
 assert "access_token" in response.json()
 assert "token_type" in response.json()

 response = client.post("/token", data={"username": "user3", "password": "password3"})
 assert response.status_code == 400
 assert response.json() == {"detail": "Incorrect username or password"}

def test_get_salary():
 response = client.post("/token", data={"username": "user1", "password": "password1"})
 token = response.json()["access_token"]

 response = client.get("/salary", headers={"Authorization": f"Bearer {token}"})
 assert response.status_code == 200
 assert response.json() == {"salary": 1000.0, "next_raise": "2023-06-01T00:00:00"}

 response = client.get("/salary", headers={"Authorization": f"Bearer invalid_token"})
 assert response.status_code == 401
 assert response.json() == {"detail": "Could not validate credentials"}
