# periodic-lambda-app
Toy application for trying out running periodic tasks on AWS Lambda.


## Installation

### Local development

Create a virtual environment and activate it:
```
python -m venv .venv
source .venv/bin/activate
```

Install `pip-tools`:
```
python -m pip install pip-tools
```

Install dependencies:
```
pip-sync requirements.txt dev-requirements.txt
```

### Docker Compose

Just start the containers:
```
docker compose up
```

## Adding dependencies

To add a dependency to a project, follow these steps:

- declare a dependency by amending `pyproject.toml`
- compile requirements file
  - for dependencies: `pip-compile -o requirements.txt pyproject.toml`
  - for dev dependencies: `pip-compile --extra=dev --output-file=dev-requirements.txt pyproject.toml`
- finally, sync your venv: `pip-sync requirements.txt dev-requirements.txt` and rebuild the containers
