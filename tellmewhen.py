import click
from server import app

@click.group()
def cli():
    """The basic commands in this thing."""
    pass

@cli.command()
def hello():
    """A basic hello world."""
    click.echo('Hello World!')

@cli.command()
def serve():
    """Run the flask server."""
    app.run()
