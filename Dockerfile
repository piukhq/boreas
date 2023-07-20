FROM ghcr.io/binkhq/python:3.11-poetry as build
WORKDIR /src

RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry self add poetry-dynamic-versioning[plugin]

ADD . .

RUN poetry build

FROM ghcr.io/binkhq/python:3.11

WORKDIR /app
COPY --from=build /src/dist/*.whl .
RUN pip install *.whl && rm *.whl

ENTRYPOINT [ "linkerd-await", "--" ]
CMD ["uvicorn", "boreas.app:create_app", "--host=0.0.0.0", "--port=6502"]
