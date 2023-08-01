"""Module providing connection to the the database."""

import logging
from contextlib import contextmanager
from datetime import datetime


logger = logging.getLogger(__name__)


class MockedSession(dict):
    """Singleton representing db session."""

    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(MockedSession, cls).__new__(cls)
        return cls.instance


# Mocked database as a singleton dict, which stores HTTP endpoints with its data.
# The structure:
# {
#     "<URL of the HTTP endpoint>": {
#         "data": "<data provided for the HTTP endpoint>",
#         "content-type": "<Content-Type provided in the Response header>"
#     }
# }
mocked_db = MockedSession()
mocked_db["endpoint/1.xml"] = {
    "data": """<menu id="file" value="File">
                    <popup>
                        <menuitem value="New" onclick="CreateNewDoc()" />
                        <menuitem value="Open" onclick="OpenDoc()" />
                        <menuitem value="Close" onclick="CloseDoc()" />
                    </popup>
                </menu>""",
    "content-type": "application/xml",
    "created": datetime(2023, 6, 1, 10, 15, 45),
}
mocked_db["endpoint/1.md5"] = {
    "data": "1e651ba4c5bcb60c6f796013d920a335",
    "content-type": "text/html",
    "created": datetime(2023, 6, 1, 10, 15, 45),
}
mocked_db["endpoint/2.json"] = {
    "data": """{"menu": {
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
    "content-type": "application/json",
    "created": datetime(2023, 7, 2, 11, 25, 55),
}


@contextmanager
def session() -> dict[str, dict]:
    try:
        yield mocked_db
    except Exception:
        logger.exception("Not connected to the database")
        raise
