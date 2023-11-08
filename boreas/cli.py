"""CLI for the Boreas Server."""
import click
import uvicorn


@click.command()
@click.option(
    "--host",
    "-h",
    type=str,
    default="127.0.0.1",
    show_default=True,
    help="Host to run the server on",
)
@click.option(
    "--port",
    "-p",
    type=int,
    default=6502,
    show_default=True,
    help="Port to run the server on",
)
@click.option(
    "--reload",
    "-r",
    type=bool,
    default=False,
    show_default=True,
    help="Enable auto-reload on code changes",
)
def cli(host: str, port: int, reload: bool) -> None:  # noqa: FBT001
    """Run a Boreas Server."""
    uvicorn.run("boreas.app:create_app", host=host, port=port, reload=reload)

cli(max_content_width=120)
