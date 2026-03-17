import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    # Arrange: Setup test client (already done)
    # Act: Call the /activities endpoint
    response = client.get("/activities")
    # Assert: Check response status and content
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert len(data) > 0


def test_signup_for_activity():
    # Arrange: Pick an activity and email
    activity_name = list(client.get("/activities").json().keys())[0]
    email = "testuser@example.com"
    # Act: Register participant
    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    # Assert: Check response status and message
    assert response.status_code == 200
    assert "message" in response.json()


def test_signup_duplicate():
    # Arrange: Pick an activity and email
    activity_name = list(client.get("/activities").json().keys())[0]
    email = "testuser@example.com"
    # Act: Register participant twice
    client.post(f"/activities/{activity_name}/signup?email={email}")
    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    # Assert: Second signup should fail
    assert response.status_code == 400
    assert "detail" in response.json()


def test_signup_invalid_activity():
    # Arrange: Use invalid activity name
    activity_name = "nonexistent"
    email = "testuser@example.com"
    # Act: Try to register
    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    # Assert: Should fail
    assert response.status_code == 404
    assert "detail" in response.json()
