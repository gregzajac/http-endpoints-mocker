# http-endpoints-mocker

Application allowes to simulate HTTP endpoints with dedicated data in various formats.

<font size="5" color="red">Project is under establishing the prototype!</font>

## Contents

* [More about project](#more-about-project)
* [Setup](#setup)
* [Technology](#technology)

## More about project

The base user story for that project is:
> As a user,
I want to create the mock of HTTP endpoint with fixed data in various formats (especially XML and JSON)
under defined URL,
So I can use it to test my tool for importing external data.

## Examples of use

1. GET info about working Nginx

    ```bash
    curl localhost:9090
    healthy
    ```

2. GET mocked data from the endpoint

    ```bash
    curl localhost:8080
    "Placeholder!"
    ```

## Setup

1. Clone repository:

    ```bash
    git clone https://github.com/gregzajac/http-endpoints-mocker.git
    ```

2. Create virtual environment and install requirements

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

Close application with command

```bash
docker compose down
```

or close with deleting volumes if needed

```bash
docker compose down -v
```

## Technology

* Python 3.11.2
* FastAPI 0.100.0
* Nginx 1.24
* Docker 24.0.5
* Docker Compose 2.3.3
