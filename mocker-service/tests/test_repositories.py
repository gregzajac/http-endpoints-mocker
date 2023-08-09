"""Tests of the repositories module."""

from datetime import datetime

import pytest

from mocker.database import session
from mocker.repositories import (
    EndpointDuplicatedError,
    EndpointNotFoundError,
    EndpointRepository,
)


def test_endpoint_repository_get_all(db):
    result = EndpointRepository(session).get_all()
    assert result == db


def test_endpoint_repository_get_by_url_success(db, example_xml):
    url, data = list(example_xml.items())[0]
    result = EndpointRepository(session).get_by_url(url)
    assert result == data


def test_endpoint_repository_get_by_url_failure_not_found(db, unknown_url):
    with pytest.raises(EndpointNotFoundError) as exc:
        EndpointRepository(session).get_by_url(unknown_url)
    assert f"Endpoint not found, URL: {unknown_url}" in str(exc.value)


def test_endpoint_repository_add_success(db, unknown_url):
    new_url = unknown_url
    new_data = {
        "content": "new content",
        "content_type": "new content type",
        "endpoint_type": "et",
    }
    EndpointRepository(session).add(
        new_url,
        new_data["content"],
        new_data["content_type"],
        new_data["endpoint_type"],
    )
    assert db[new_url]["content"] == new_data["content"]
    assert db[new_url]["content_type"] == new_data["content_type"]
    assert db[new_url]["endpoint_type"] == new_data["endpoint_type"]
    assert isinstance(db[new_url]["created"], datetime)


def test_endpoint_repository_add_failure_duplicated(db, example_xml):
    url, data = list(example_xml.items())[0]
    with pytest.raises(EndpointDuplicatedError) as exc:
        EndpointRepository(session).add(
            url,
            data["content"],
            data["content_type"],
            data["endpoint_type"],
        )
    assert f"Endpoint already exists, URL: {url}" in str(exc.value)


def test_endpoint_repository_remove_success(db, example_json):
    url, data = list(example_json.items())[0]
    removed = EndpointRepository(session).remove(url)
    assert db.get(url) is None
    assert removed["content"] == data["content"]
    assert removed["content_type"] == data["content_type"]
    assert removed["endpoint_type"] == data["endpoint_type"]


def test_endpoint_repository_remove_failure_not_found(db, unknown_url):
    with pytest.raises(EndpointNotFoundError) as exc:
        EndpointRepository(session).remove(unknown_url)
    assert f"Endpoint not found, URL: {unknown_url}" in str(exc.value)
