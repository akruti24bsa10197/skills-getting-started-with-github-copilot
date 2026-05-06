import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

# Helper to reset activities state if needed (depends on app implementation)

def test_successful_signup():
    # Arrange
    activity = list(client.get("/activities").json().keys())[0]
    email = "testuser1@mergington.edu"
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 200
    assert "message" in response.json()
    # Confirm participant is in the list
    activities = client.get("/activities").json()
    assert email in activities[activity]["participants"]

def test_duplicate_signup():
    # Arrange
    activity = list(client.get("/activities").json().keys())[0]
    email = "testuser2@mergington.edu"
    client.post(f"/activities/{activity}/signup?email={email}")
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 400
    assert "detail" in response.json()

def test_fetch_activities():
    # Arrange & Act
    response = client.get("/activities")
    # Assert
    assert response.status_code == 200
    activities = response.json()
    assert isinstance(activities, dict)
    assert len(activities) > 0
