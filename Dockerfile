FROM ghcr.io/binkhq/python:3.11 as build
WORKDIR /src

RUN apt update && apt -y install git
RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry self add poetry-dynamic-versioning[plugin]

ADD . .

RUN poetry build

FROM ghcr.io/binkhq/python:3.11

WORKDIR /app
COPY --from=build /src/dist/*.whl .
RUN pip install *.whl && rm *.whl

CMD ["uvicorn", "boreas.app:create_app", "--host=0.0.0.0", "--port=6502"]
