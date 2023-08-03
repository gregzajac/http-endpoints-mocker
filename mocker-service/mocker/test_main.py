"""Tests module."""

from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from mocker.db import mocked_db
from mocker.main import app
from mocker.repositories import EndpointNotFoundError


@pytest.fixture
def client():
    yield TestClient(app)


@pytest.fixture
def db():
    return mocked_db


def test_read_main(client):
    """
    GIVEN a test client to the API
    WHEN a Request is send to the root URL
    THEN obtain a Response with a status code 200 OK
    and with Content-Type "application/json"
    and with a placeholder text
    """
    response = client.get("/")
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    assert response.json() == "Placeholder!"


def test_get_by_url_success(client, db):
    """
    GIVEN a test client to the API
    and an access to the test database
    WHEN a Request is send to the URL existing in the database
    THEN obtain a Response with a status code 200 OK
    and with correct Content-Type in a Response header
    and with correct URL data
    """
    url, url_data = db.popitem()

    with patch(
        "mocker.repositories.endpoint_repository.get_by_url", return_value=url_data
    ):
        response = client.get("/api/" + url)

    assert response.status_code == 200
    assert response.headers["Content-Type"] == url_data["content_type"]
    assert response.content.decode() == url_data["content"]


def test_get_by_url_failure_not_found_url(client):
    """
    GIVEN a test client to the API
    WHEN a Request is send to the URL not existing in the database
    THEN obtain a Response with a status code 404 NOT FOUND
    """
    wrong_url = "some-wrong-url/next-part/1.xml"

    with patch(
        "mocker.repositories.endpoint_repository.get_by_url",
        side_effect=EndpointNotFoundError(wrong_url),
    ):
        response = client.get(wrong_url)

    assert response.status_code == 404
