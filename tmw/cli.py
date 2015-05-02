import click
from server import app
import core

@click.group()
def cli():
    """The basic commands in this thing."""
    pass

@cli.command()
@click.option('--url', prompt='URL', help='URL to watch')
@click.option('--check_type', prompt='Type of check',
        type=click.Choice(core.event_types), 
        help='Type of check to perform')
@click.option('--check_value', prompt='Check value',
        help='Expected value to alert on')
@click.option('--frequency', default=10,
        help='Frequency to check (in seconds)')
@click.option('--num_checks', prompt='Number of checks:', 
        help='How many times to check (0 is infinite)', default=1)
def tellme(url, check_type, check_value, frequency, num_checks):
    """Check a url to see if it matches"""

    click.echo('Telling you if {0} has a {1} that matches {2}'.format(
        click.style(url, bg='blue', fg='white'), 
        click.style(check_type, bg='blue', fg='white'), 
        click.style(check_value, bg='blue', fg='white')))

    try:
        check_results = core.check_until(url, check_type, check_value,
                frequency, num_checks)
        if check_results:
            click.secho('It does!', bg='green', fg='white')
        else:
            click.secho('It does NOT!', bg='red', fg='white')

    except core.TMWCoreException, e:
        click.secho('ERROR: %s' % e.message, fg='red', bold=True)

@cli.command()
def hello():
    """A basic hello world."""
    click.echo('Hello World Again!')

@cli.command()
def bye():
    """The opposite of hello world."""
    click.echo('Goodbye cruel world.......')

@cli.command()
def serve():
    """Run the flask server."""
    app.run()

@cli.command()
def debug():
    app.debug = True
    app.run()
