"""Repositories module."""

from contextlib import AbstractContextManager
from datetime import datetime
from typing import Callable

from mocker.database import session


class EndpointRepository:
    """API of the Endpoint repository."""

    def __init__(
        self,
        session_factory: Callable[..., AbstractContextManager[dict]],
    ) -> None:
        self.session_factory = session_factory

    def get_all(self) -> str:
        with self.session_factory() as session:
            return session

    def get_by_url(self, url: str) -> dict:
        with self.session_factory() as session:
            endpoint_data = session.get(url)
            if not endpoint_data:
                raise EndpointNotFoundError(url)
            return endpoint_data

    def add(
        self, url: str, content: str, content_type: str, endpoint_type: str
    ) -> None:
        with self.session_factory() as session:
            endpoint = session.get(url)
            if endpoint:
                raise EndpointDuplicatedError(url)
            data = {
                "content": content,
                "content_type": content_type,
                "endpoint_type": endpoint_type,
                "created": datetime.now(),
            }
            session.update({url: data})

    def remove(self, url: str):
        with self.session_factory() as session:
            endpoint = session.get(url)
            if not endpoint:
                raise EndpointNotFoundError(url)
            removed = session.pop(url)
            return removed


class EndpointNotFoundError(Exception):
    """The endpoint was not found in the repository."""

    def __init__(self, endpoint_url):
        super().__init__(f"Endpoint not found, URL: {endpoint_url}")


class EndpointDuplicatedError(Exception):
    """The endpoint already exists in the repository."""

    def __init__(self, endpoint_url):
        super().__init__(f"Endpoint already exists, URL: {endpoint_url}")


# endpoint_repository = EndpointRepository(session)
