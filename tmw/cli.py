
import json
import os

import click
import keyring

import config
import core
from notify import channels, notify
from server import app

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

    if not config._exists():
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

        if config._exists():
            event = '{0} had a "{1}" that {2} "{3}" after {4} check{5}'.format(
                    url, check_type,
                    'matched' if check_results else 'did not match',
                    check_value, total_checks,
                    's' if total_checks > 1 else '')
            
            click.echo('Sending notifications ...')
            notify(event)

    except core.TMWCoreException, e:
        click.secho('ERROR: %s' % e.message, fg='red', bold=True)

@cli.command()
@click.option('--force', is_flag=True,
    help='Force configuration (i.e. redo an existing one)')
def configure_notifications(force):
    """Configure notification settings (e.g. smtp/slack settings)"""

    if config._exists():
        if not force:
            click.echo('Config already exists - try again with --force')
            return
        else:
            click.echo('Replacing existing config')

    config = {}
    keyring_config = {}
    any_channel = False
    click.secho('## Notification Configuration ##', bg='blue', fg='white', bold=True)
    for channel in channels.keys():
        
        enable = click.prompt('Enable {0} channel? (y/n)'.format(channel), 
            type=bool)
        
        if enable:

            any_channel = True

            config[channel] = {}

            click.secho('### {0} ###'.format(channel), bg='blue', fg='white')
            for f in channels[channel]['fields']:

                value = click.prompt(
                        '  %s' % f['name'], 
                        type=f['type'], 
                        default=f['default'],
                        hide_input=f.get('hide_input', False),
                    )

                if f.get('hide_input', False):
                    keyring_config['{0}:{1}'.format(channel, f['name'])] = value
                    config[channel][f['name']] = None
                else:
                    config[channel][f['name']] = value

            if keyring_config:
                click.echo('Saving sensitive data to keyring')
                for k,v in keyring_config.iteritems():
                    keyring.set_password(config.KEYRING_SVC, k, v)


    if any_channel:
        click.echo('Saving config file {0}'.format(config.CFG_FILE))
        with open(config.CFG_FILE, 'w') as f:
            f.write(json.dumps(config, indent=4))
    else:
        click.secho('WARNING: No channels enabled - not writing config', 
                bg='yellow', fg='black')


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
