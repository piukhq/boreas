FROM ghcr.io/binkhq/python:3.10-poetry as build
WORKDIR /src

RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry self add poetry-dynamic-versioning[plugin]

ADD . .

RUN poetry build

FROM ghcr.io/binkhq/python:3.10

WORKDIR /app
COPY --from=build /src/dist/*.whl .
COPY --from=build /src/asgi.py .
RUN pip install *.whl && rm *.whl

ENTRYPOINT [ "linkerd-await", "--" ]
CMD ["sh", "-c", "uvicorn asgi:app --host 0.0.0.0 --port 8001 & uvicorn asgi:app --host 0.0.0.0 --port 9100"]
