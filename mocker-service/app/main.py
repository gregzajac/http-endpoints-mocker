from fastapi import FastAPI, Response, status

from config import settings
from repositories import EndpointNotFoundError, endpoint_repository


app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)


@app.get("/", tags=["Test HTTP endpoint"])
def home():
    return "Placeholder!"


@app.get("/api/{url:path}", tags=["Get endpoint by URL"])
def get_endpoint(url: str):
    try:
        endpoint = endpoint_repository.get_by_url(url)
        return Response(content=endpoint["data"], media_type=endpoint["content-type"])
    except EndpointNotFoundError:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
