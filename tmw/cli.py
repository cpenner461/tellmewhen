
import json
import os

import click
import keyring

import core
from notify import notification_types, smtp_send
from server import app

CFG_FILE = os.path.expanduser("~/.tellmewhen")
KEYRING_SVC = "tellmewhen"

def _config_exists():
    """Verify if a config file exists"""
    return os.path.exists(CFG_FILE)

def _load_config():
    """Load the config file"""
    if _config_exists():
        return json.loads(open(CFG_FILE, 'r').read())

    return None

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

    if not _config_exists():
        click.secho('WARNING: No config file found, notifications will not be sent',
                bg='yellow', fg='black')

    click.echo('Telling you if {0} has a {1} that matches {2}'.format(
        click.style(url, bg='blue', fg='white'), 
        click.style(check_type, bg='blue', fg='white'), 
        click.style(check_value, bg='blue', fg='white')))

    try:
        (check_results, total_checks) = core.check_until(url, check_type, check_value,
                frequency, num_checks)

        if check_results:
            click.secho('It does!', bg='green', fg='white')
        else:
            click.secho('It does NOT!', bg='red', fg='white')

        if _config_exists():
            event = '{0} had a "{1}" that {2} "{3}" after {4} check{5}'.format(
                    url, check_type,
                    'matched' if check_results else 'did not match',
                    check_value, total_checks,
                    's' if total_checks > 1 else '')
            
            click.echo('Sending notification ...')
            smtp_send(event, _load_config())

    except core.TMWCoreException, e:
        click.secho('ERROR: %s' % e.message, fg='red', bold=True)

@cli.command()
@click.option('--force', is_flag=True,
    help='Force configuration (i.e. redo an existing one)')
def configure_notifications(force):
    """Configure notification settings (e.g. smtp/slack settings)"""

    if os.path.exists(CFG_FILE):
        if not force:
            click.echo('Config already exists - try again with --force')
            return
        else:
            click.echo('Replacing existing config')

    click.secho('## Notification Configuration ##', bg='blue', fg='white', bold=True)

    valid_types = notification_types.keys()
    notification_type = None
    while notification_type not in valid_types:

        notification_type = click.prompt('Enter type of notification',
            default=valid_types[0])
        if notification_type not in valid_types:
            click.secho('Invalid type, must be one of %s' % valid_types,
                    bg='red', fg='white', bold=True)
  
    config = {}
    keyring_config = {}
    for f in notification_types[notification_type]['fields']:

        value = click.prompt(
                '  %s' % f['name'], 
                type=f['type'], 
                default=f['default'],
                hide_input=f.get('hide_input', False),
            )

        if f.get('hide_input', False):
            keyring_config[f['name']] = value
            config[f['name']] = None
        else:
            config[f['name']] = value

    if keyring_config:
        click.echo('Saving sensitive data to keyring')
        for k,v in keyring_config.iteritems():
            keyring.set_password(KEYRING_SVC, k, v)

    click.echo('Saving config file {0}'.format(CFG_FILE))
    with open(CFG_FILE, 'w') as f:
        f.write(json.dumps(config, indent=4))


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
