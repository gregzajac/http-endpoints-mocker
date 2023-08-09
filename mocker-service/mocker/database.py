"""Database module."""

import logging
from contextlib import contextmanager
from datetime import datetime
from typing import Generator


logger = logging.getLogger(__name__)


class DbStorage(dict):
    """A Singleton dictionary representing a key-value database.

    The structure of the Endpoint:
    - key (str): Endpoint URL,
    - value (dict): Endpoint data, with the structure:
        - "content" (str): Data provided for the Endpoint,
        - "content_type" (str): Content-Type provided in the Response header,
        - "endpoint_type" (str): Allowed Endpoint type (XML/JSON),
        - "created" (datetime): Date and time of the endpoint creation.
    """

    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(DbStorage, cls).__new__(cls)
        return cls.instance


db_example_xml = {
    "sub-url/file.xml": {
        "content": """<menu id="file" value="File">
    <popup>
        <menuitem value="New" onclick="CreateNewDoc()" />
        <menuitem value="Open" onclick="OpenDoc()" />
        <menuitem value="Close" onclick="CloseDoc()" />
    </popup>
</menu>""",
        "content_type": "application/xml",
        "endpoint_type": "XML",
        "created": datetime(2023, 6, 1, 10, 15, 45),
    },
}

db_example_md5 = {
    "sub-url/file.md5": {
        "content": "1e651ba4c5bcb60c6f796013d920a335",
        "content_type": "text/html",
        "endpoint_type": "XML",
        "created": datetime(2023, 6, 1, 10, 15, 45),
    },
}

db_example_json = {
    "sub-url/file.json": {
        "content": """{"menu": {
    "id": "file",
    "value": "File",
    "popup": {
        "menuitem": [
            {"value": "New", "onclick": "CreateNewDoc()"},
            {"value": "Open", "onclick": "OpenDoc()"},
            {"value": "Close", "onclick": "CloseDoc()"}
        ]
    }
}}""",
        "content_type": "application/json",
        "endpoint_type": "JSON",
        "created": datetime(2023, 7, 2, 11, 25, 55),
    },
}


def add_data_to_db(db: DbStorage, db_data: dict[str, dict]) -> None:
    for key, value in db_data.items():
        db[key] = value


def clear_db(db: DbStorage) -> None:
    db.clear()


db_storage = DbStorage()
# add_data_to_db(db_storage, db_example_xml | db_example_md5 | db_example_json)


@contextmanager
def session() -> Generator:
    try:
        yield db_storage
    except Exception:
        logger.exception("Not connected to the database")
        raise
