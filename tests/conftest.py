import pytest
from fastapi.testclient import TestClient

# Importa a instância correta do FastAPI
from src.api.app import app


@pytest.fixture
def client():
    """Fixture que retorna um TestClient para a aplicação FastAPI."""
    return TestClient(app)

