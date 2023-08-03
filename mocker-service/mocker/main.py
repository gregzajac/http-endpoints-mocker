"""Main module."""

from fastapi import FastAPI, Response, status

from mocker.config import settings
from mocker.repositories import EndpointNotFoundError, endpoint_repository


app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)


@app.get("/", tags=["Test HTTP endpoint"])
def home():
    return "Placeholder!"


@app.get(
    "/api/{url:path}",
    tags=["Get the endpoint by the given URL"],
)
def get_endpoint(url: str):
    try:
        url_data = endpoint_repository.get_by_url(url)
        return Response(
            content=url_data["content"], media_type=url_data["content_type"]
        )
    except EndpointNotFoundError:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
