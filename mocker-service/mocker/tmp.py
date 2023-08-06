from database import db_storage, session
from repositories import EndpointRepository, endpoint_repository


print(db_storage)
# endpoint_repository = EndpointRepository(session)
print(endpoint_repository)

endpoint_repository.add(
    "nowyurl.xml",
    "<tag>zawartość</tag>",
    "application/xml",
    "xml",
)
print(db_storage)
