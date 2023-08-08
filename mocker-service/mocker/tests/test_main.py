"""Tests of the main module."""


from fastapi import FastAPI

from mocker.database import db_example_json, db_example_xml
from mocker.main import app


def test_app():
    assert isinstance(app, FastAPI)


def test_get_root(client):
    """
    GIVEN a test client to the API
    WHEN send a GET Request to the root URL
    THEN obtain a Response with status code 200 OK
    and obtain a Response with Content-Type "application/json"
    and obtain a Response with a placeholder text
    """
    response = client.get("/")
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    assert response.json() == "Placeholder!"


def test_get_endpoints(client):
    """
    GIVEN a test client to the API
    WHEN send a GET Request to the `endpoints/` URL
    THEN obtain a Response with a status code 200 OK
    and obtain a Response with Content-Type "application/json"
    and obtain a Response with mocked database data.
    """
    response = client.get("/endpoints/")
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    assert len(response.json()) == 3


def test_get_endpoint_success(client, example_xml):
    """
    GIVEN a test client to the API
    WHEN send a GET Request to the existing URL with XML
    THEN obtain a Response with a status code 200 OK
    and obtain a Response with Content-Type "application/xml"
    and obtain a Response with XML data.
    """
    url, data = list(example_xml.items())[0]

    response = client.get("/endpoints/" + url)

    assert response.status_code == 200
    assert response.headers["Content-Type"] == data["content_type"]
    assert response.content.decode() == data["content"]


def test_get_endpoint_failure_not_found_url(client, unknown_url):
    """
    GIVEN a test client to the API
    WHEN send a GET Request to the unknown URL with XML
    THEN obtain a Response with a status code 404 NOT FOUND
    """
    response = client.get(unknown_url)

    assert response.status_code == 404


def test_add_endpoint_xml_success(client):
    """
    GIVEN a test client to the API
    WHEN send a POST Request to the new URL with XML
    THEN obtain a Response with a status code 201 CREATED
    and obtain a Response with Content-Type "text/html; charset=utf-8"
    and new URL with XML exists in Response
    and MD5 URL from XML URL exists in Response
    """
    new_xml_url = "sub-url/newfile.xml"
    url_md5_from_xml = "sub-url/newfile.md5"

    post_data = {
        "url": new_xml_url,
        "content": "content for new xml",
        "endpoint_type": "XML",
    }
    response = client.post("/endpoints/", json=post_data)

    assert response.status_code == 201
    assert response.headers["Content-Type"] == "text/html; charset=utf-8"
    assert new_xml_url in response.content.decode()
    assert url_md5_from_xml in response.content.decode()


def test_add_endpoint_xml_failure_endpoint_already_exists(client):
    """
    GIVEN a test client to the API
    WHEN send a POST Request to the existing URL with XML
    THEN obtain a Response with a status code 409 Conflict
    """
    url, data = list(db_example_xml.items())[0]

    post_data = {
        "url": url,
        "content": data["content"],
        "endpoint_type": "XML",
    }
    response = client.post("/endpoints/", json=post_data)

    assert response.status_code == 409


def test_add_endpoint_json_success(client):
    """
    GIVEN a test client to the API
    WHEN send a POST Request to the new URL with JSON
    THEN obtain a Response with a status code 201 CREATED
    and obtain a Response with Content-Type "text/html; charset=utf-8"
    and new URL with XML exists in Response
    and MD5 URL from XML URL exists in Response
    """
    new_json_url = "sub-url/newfile.json"

    post_data = {
        "url": new_json_url,
        "content": "content for new xml",
        "endpoint_type": "XML",
    }
    response = client.post("/endpoints/", json=post_data)

    assert response.status_code == 201
    assert response.headers["Content-Type"] == "text/html; charset=utf-8"
    assert new_json_url in response.content.decode()


def test_add_endpoint_json_failure_endpoint_already_exists(client):
    """
    GIVEN a test client to the API
    WHEN send a POST Request to the existing URL with JSON
    THEN obtain a Response with a status code 409 Conflict
    """
    url, data = list(db_example_json.items())[0]

    post_data = {
        "url": url,
        "content": data["content"],
        "endpoint_type": "XML",
    }
    response = client.post("/endpoints/", json=post_data)

    assert response.status_code == 409


# TODO: test_add_endpoint_xml_failure_cannot_create_md5
