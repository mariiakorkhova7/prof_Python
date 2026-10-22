import pytest
from fastapi.testclient import TestClient
from grade_service.api import app

@pytest.fixture
def client():
    return TestClient(app)