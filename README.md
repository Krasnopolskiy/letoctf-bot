# CTF Platform Bot

## Local Setup

### Setup Secrets

Copy and edit `.env` file with preferred values

```shell
cp deploy/config/.env.sample deploy/config/.env
source deploy/config/.env
```

### Setup Environment

Make sure your system has `poetry` and `python3.12` installed

```shell
poetry env use python3
poetry shell
poetry install
```

### Start Services

Make sure your system has `docker` installed

```shell
docker compose -f deploy/docker-compose.yaml up -d mysql redis
```

### Start Bot

```shell
python3 bot/main.py
```

## Docker Setup

### Setup Secrets

Copy and edit `.env` file with preferred values

```shell
cp deploy/config/.env.sample deploy/config/.env
source deploy/config/.env
```

### Start Services

Make sure your system has `docker` installed

```shell
docker compose -f deploy/docker-compose.yaml up -d
```
