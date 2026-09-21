import pytest

from fastapi.testclient import TestClient

from database.FastAPI import app
from database.connection import get_db


class FakeResult:
    def __init__(self, scalar_value=None):
        self.scalar_value = scalar_value

    def scalar(self):
        return self.scalar_value


class FakeDatabaseSession:
    def __init__(self):
        self.executed_queries = []

    def execute(self, query):
        query_text = str(query)

        self.executed_queries.append(query_text)

        if "COUNT(*)" in query_text:
            return FakeResult(scalar_value=19735)

        return FakeResult()


@pytest.fixture
def fake_db():
    return FakeDatabaseSession()


@pytest.fixture
def client(fake_db):
    def override_get_db():
        yield fake_db

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


def test_health_endpoint(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "Running"
    }


def test_database_endpoint(client, fake_db):
    response = client.get("/test-db")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Database connected!"
    }

    assert any(
        "SELECT 1" in query
        for query in fake_db.executed_queries
    )


def test_table_endpoint(client, fake_db):
    response = client.get("/test-table")

    assert response.status_code == 200
    assert response.json() == {
        "rows": 19735
    }

    assert any(
        "COUNT(*)" in query
        for query in fake_db.executed_queries
    )