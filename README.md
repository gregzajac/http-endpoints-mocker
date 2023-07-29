# http-endpoints-mocker


## Spis treści

* [Opis projektu](#opis-projektu)
* [Instalacja](#instalacja)
* [Uruchomienie](#uruchomienie)
* [Technologia](#technologia)

## Opis projektu

Aplikacja umożliwia wystawianie danych w formacie XML lub JSON pod zadanym adresem URL.

## Instalacja

1. Sklonowanie repo: 

    ```bash
    git clone https://github.com/gregzajac/http-endpoints-mocker.git
    ```

2. Utworzenie w projekcie środowiska wirtualnego

    ```bash
    cd http http-endpoints-mocker
    python -m venv venv
    ```

3. instalacja bibliotek trzecich w utworzonym środowisku virtualnym

    ```bash
    source venv/bin/activate
    pip install -r requirements.txt
    ```

## Uruchomienie

1. Środowisko uruchamiamy komendą

    ```bash
    docker compose up -d
    ```

2. Środowisko zamykamy komendą

    ```bash
    docker compose up -d
    ```

### Info

Zamknięcie środowiska z usunięciem voluminów danych

```bash
docker compose down -v
```

## Technologia

* Python 3.11.2
* FastAPI 0.100.0
* Nginx 1.24
