"""Tests module."""

from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from mocker.db import mocked_db
from mocker.main import app


@pytest.fixture
def client():
    yield TestClient(app)


@pytest.fixture
def db():
    return mocked_db


def test_read_main(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    assert response.json() == "Placeholder!"


def test_get_by_url_correct(client, db):
    url, url_data = db.popitem()

    with patch(
        "mocker.repositories.endpoint_repository.get_by_url", return_value=url_data
    ):
        response = client.get("/api/" + url)

    assert response.status_code == 200
    assert response.headers["Content-Type"] == url_data["content_type"]
    assert response.content.decode() == url_data["content"]
