"""Pytest fixtures."""

import pytest
from fastapi.testclient import TestClient

from mocker.database import (
    add_data_to_db,
    db_example_json,
    db_example_md5,
    db_example_xml,
    db_storage,
    remove_data_from_db,
)
from mocker.main import app


@pytest.fixture
def db():
    try:
        examples = db_example_xml | db_example_md5 | db_example_json
        add_data_to_db(db_storage, examples)
        yield db_storage
    finally:
        remove_data_from_db(db_storage)


@pytest.fixture
def client(db):
    yield TestClient(app)


@pytest.fixture
def example_xml():
    return db_example_xml


@pytest.fixture
def example_md5():
    return db_example_md5


@pytest.fixture
def example_json():
    return db_example_json


@pytest.fixture
def unknown_url():
    return "some-wrong-url/next-part/1.xml"
