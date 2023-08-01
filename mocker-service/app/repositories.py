"""Concrete API implementations, based on given database."""

from contextlib import AbstractContextManager
from typing import Callable

from db import session


class EndpointRepository:
    """Implementation of the Endpoint API."""

    def __init__(
        self,
        session_factory: Callable[..., AbstractContextManager[dict]],
    ) -> None:
        self.session_factory = session_factory

    def get_all(self) -> str:
        with self.session_factory() as session:
            return session

    def get_by_url(self, url: str) -> dict[str, dict]:
        with self.session_factory() as session:
            endpoint = session.get(url)
            if not endpoint:
                raise EndpointNotFoundError(url)
            return endpoint

    def add(self, url: str, data: dict) -> dict[str, dict]:
        with self.session_factory() as session:
            endpoint = session.get(url)
            if endpoint:
                raise EndpointDuplicatedError(url)
            session.update({url: data})


class EndpointNotFoundError(Exception):
    """Endpoint was not found in the repository."""

    def __init__(self, endpoint_url):
        super().__init__(f"Endpoint not found, id: {endpoint_url}")


class EndpointDuplicatedError(Exception):
    """Endpoint with this URL already exists in the repository."""

    def __init__(self, endpoint_url):
        super().__init__(f"Endpoint with this URL already exists, id: {endpoint_url}")


endpoint_repository = EndpointRepository(session)
