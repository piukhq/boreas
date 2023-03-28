FROM ghcr.io/binkhq/python:3.10-poetry as build
WORKDIR /src
ADD . .
RUN poetry build

FROM ghcr.io/binkhq/python:3.10
WORKDIR /app
COPY --from=build /src/dist/*.whl .

RUN pip install *.whl && rm *.whl
COPY --from=build /src/asgi.py .
COPY --from=build /src/boreas/dlx_consumer.py .

ENTRYPOINT [ "linkerd-await", "--" ]
CMD ["uvicorn", "asgi:app", "--host", "0.0.0.0", "--port", "8001"]
