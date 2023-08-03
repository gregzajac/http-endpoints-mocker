# http-endpoints-mocker

Application allowes to simulate HTTP endpoints with dedicated data in various formats.

<font size="5" color="red">Project is under establishing the prototype!</font>

## Contents

* [More about project](#more-about-project)
* [Examples of use](#examples-of-use)
* [Setup](#setup)
* [Technology](#technology)

## More about project

The base user story for that project is:
> As a user,
I want to create the mock of HTTP endpoint with fixed data in various formats (especially XML and JSON)
under defined URL,
So I can use it to test my tool for importing external data.

## Examples of use

1. GET info from Nginx:

    ```bash
    $ curl localhost:9090
    healthy
    ```

2. GET mocked XML:

    ```bash
    $ curl localhost:8080/api/sub-url/file.xml
    <menu id="file" value="File">
        <popup>
            <menuitem value="New" onclick="CreateNewDoc()" />
            <menuitem value="Open" onclick="OpenDoc()" />
            <menuitem value="Close" onclick="CloseDoc()" />
        </popup>
    </menu>
    ```

3. GET mocked JSON:

    ```bash
    $ curl localhost:8080/api/sub-url/file.json
    {"menu": {
        "id": "file",
        "value": "File",
        "popup": {
            "menuitem": [
                {"value": "New", "onclick": "CreateNewDoc()"},
                {"value": "Open", "onclick": "OpenDoc()"},
                {"value": "Close", "onclick": "CloseDoc()"}
            ]
        }
    }}
    ```

## Setup

1. Clone repository:

    ```bash
    git clone https://github.com/gregzajac/http-endpoints-mocker.git
    ```

2. Create virtual environment and install requirements:

    ```bash
    cd http http-endpoints-mocker
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

3. Run application

    ```bash
    docker compose up -d
    ```

### Note

Run tests with command:

```bash
docker compose exec mocker pytest -p no:cacheprovider
```

Close the application with command:

```bash
docker compose down
```

or close with deleting volumes if needed:

```bash
docker compose down -v
```

## Technology

* Python 3.11
* FastAPI 0.100.0
* Pytest 7.4.0
* Nginx 1.24
* Docker 24.0.5
* Docker Compose 2.3.3
