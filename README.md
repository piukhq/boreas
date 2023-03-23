# Harmonia Transactions API 
Harmonia Transactions API is a simple service allowing Harmonia to accept transactions from merchants via an API.

### Pre-requisites
* Python >= 3.10
* [poetry](https://python-poetry.org/docs/master/) 

### Configuration
The project is configured through environment variables. A convenient way
of setting these is via the `.env` file found in the project root. See `settings.py` for
configuration options that can be set in this file.

Your code editor should support loading environment variables from the `.env`
file either out of the box or with a plugin. For shell usages, you can have poetry
automatically load these environment variables by using
[poetry-dotenv-plugin](https://github.com/mpeteuil/poetry-dotenv-plugin), or
use a tool like [direnv](https://direnv.net/).

### Running the Project
```bash
uvicorn asgi:app --host 0.0.0.0 --port 8001
python dlx_consumer.py
```

The consumer is used for retrying queued transactions that for whatever reason didn't make it into Harmonia.

### Deployment
There is a Dockerfile provided in the project root. Build an image from this to
get a deployment-ready version of the project.

### Unit Tests
```bash
pytest tests
```
Tests will be autodiscovered.