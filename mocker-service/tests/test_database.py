from datetime import datetime

from mocker.database import add_data_to_db, clear_db, db_storage


def test_add_data_to_db_and_clear_success(example_json):
    url, data = list(example_json.items())[0]

    add_data_to_db(db_storage, example_json)

    assert db_storage[url]["content"] == data["content"]
    assert db_storage[url]["content_type"] == data["content_type"]
    assert db_storage[url]["endpoint_type"] == data["endpoint_type"]
    assert isinstance(db_storage[url]["created"], datetime)

    clear_db(db_storage)

    assert db_storage == {}
