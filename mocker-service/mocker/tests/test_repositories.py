"""Tests of the repositories module."""

import pytest
from mocker.database import session
from mocker.repositories import (
    EndpointRepository,
    EndpointNotFoundError,
    EndpointDuplicatedError,
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
