## Python Scripts
This is a Docker container that can be used to run Python scripts.

## Run container in bash mode
```sh
docker-compose run --rm --name python-scripts python-scripts bash
```

## Run a python script directly
```sh
docker-compose run --rm --name python-scripts python-scripts python3 sample.py
```