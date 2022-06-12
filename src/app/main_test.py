from fastapi.testclient import TestClient
from main import app
import pytest 

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}

def test_count_posts():
    response = client.get("/count_posts")
    assert response.status_code == 200
    print(response.json()) 
