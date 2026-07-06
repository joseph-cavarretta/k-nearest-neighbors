import pytest
from fastapi.testclient import TestClient

from src.app.api import create_app
from src.config.settings import Settings


@pytest.fixture()
def settings() -> Settings:
    return Settings(max_points_per_list=100)


@pytest.fixture()
def client(settings: Settings) -> TestClient:
    return TestClient(create_app(settings))
