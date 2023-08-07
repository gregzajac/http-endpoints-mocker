"""Main module."""

import hashlib
import logging
from typing import Annotated

from fastapi import Body, FastAPI, HTTPException, Response, status

from mocker.config import settings
from mocker.database import session
from mocker.repositories import (
    EndpointDuplicatedError,
    EndpointNotFoundError,
    EndpointRepository,
)


logger = logging.getLogger(__name__)


app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)

endpoint_repository = EndpointRepository(session)


@app.get("/", tags=["Get root"])
def get_root():
    return "Placeholder!"


@app.get(
    "/endpoints/",
    tags=["Get all Endpoints"],
)
def get_endpoints():
    endpoints = endpoint_repository.get_all()
    return endpoints


@app.get(
    "/endpoints/{url:path}",
    tags=["Get Endpoint by URL"],
)
def get_endpoint(url: str):
    try:
        url_data = endpoint_repository.get_by_url(url)
        return Response(
            content=url_data["content"], media_type=url_data["content_type"]
        )
    except EndpointNotFoundError as err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))


@app.post(
    "/endpoints/",
    tags=["Create Endpoint"],
)
def add_endpoint(
    url: Annotated[str, Body()],
    content: Annotated[str, Body()],
    endpoint_type: Annotated[str, Body()],
):
    """Add new endpoint (for XML add additional MD5 endpoint).

    Args:
        url (str): URL of the HTTP endpoint
        content (str): data provided for the HTTP endpoint
        endpoint_type (str): xml or json

    Returns:
        list[str]: A list of created URLs of the HTTP endpoints (one for JSON,
        two for XML)
    """
    if endpoint_type.upper() == "XML":
        # Add the XML Endpoint
        try:
            endpoint_repository.add(url, content, "application/xml", endpoint_type)

            # Add the MD5 Endpoint for the previously added XML Endpoint
            url_md5 = _create_url_with_md5_extension(url)
            url_md5_content = hashlib.md5(content.encode()).hexdigest()
            try:
                endpoint_repository.add(
                    url_md5, url_md5_content, "text/html", endpoint_type
                )
            except EndpointDuplicatedError:
                # Remove a previously added XML Endpoint due to not added MD5 Endpoint
                logger.critical(
                    f"Cannot add MD5 Endpoint `{url_md5}` "
                    f"even if corresponding XML Endpoint `{url}` has been added"
                )
                try:
                    endpoint_repository.remove(url)
                except EndpointNotFoundError:
                    logger.critical(
                        f"Cannot remove previously added XML endpoint `{url}`"
                    )

            return Response(
                content=f"Utworzone endpointy:\n{[url, url_md5]}",
                status_code=status.HTTP_201_CREATED,
                media_type="text/html",
            )

        except EndpointDuplicatedError as err:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(err))

    if endpoint_type.upper() == "JSON":
        try:
            endpoint_repository.add(url, content, "application/json", endpoint_type)
            return Response(
                content=f"Utworzone endpointy:\n{[url]}",
                status_code=status.HTTP_201_CREATED,
                media_type="text/html",
            )
        except EndpointDuplicatedError as err:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(err))

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=f"Not allowed endpoint type `{endpoint_type}`",
    )


def _create_url_with_md5_extension(url: str) -> str:
    """From given URL, create the one with the `.md5` extension.

    Args:
        url (str): Endpoint URL (can have only one dot as a file extension)

    Returns:
        str: Endpoint URL with changed extension to `.md5` (or added if file name
            in the URL Endpoint didn't have it)
    """
    url_sections = url.split("/")
    last_section = url_sections[-1]
    last_section_dot_parts = last_section.split(".")

    if len(last_section_dot_parts) == 2:
        last_section = last_section_dot_parts[0] + ".md5"
    else:
        last_section = last_section + ".md5"
    url_sections[-1] = last_section

    return "/".join(url_sections)
