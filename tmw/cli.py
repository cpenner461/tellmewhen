'''

This is the command line interface to tmw.  Usage is self documenting via built
in help (e.g. `tmw --help`).
'''

import itertools
import json
from multiprocessing import Pool
import sys
import time

import click
import keyring
from requests.exceptions import ConnectionError

import tmw.config as config
import tmw.core as core
from tmw.notify import channels, tell
from tmw.server import app

pool = Pool(processes=2)

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

    if not config.exists():
        click.secho('WARNING: No config file found, notifications will not be sent',
                bg='yellow', fg='black')

    click.echo('Telling you if {0}\n  has a {1}\n  that matches {2} ... '.format(
        click.style(url, bg='blue', fg='white'), 
        click.style(check_type, bg='blue', fg='white'), 
        click.style(check_value, bg='blue', fg='white')),
        nl=False)

    try:

        check_results = None
        total_checks = None

        def _handle_results(results):
            (check_results, total_checks) = results
            if check_results:
                click.secho('YES!', bg='green', fg='white')
            else:
                click.secho('NO!', bg='red', fg='white')

        job = pool.apply_async(
            core.check_until, 
            (url, check_type, check_value, frequency, num_checks),
            callback=_handle_results)

        spinner = itertools.cycle(['-', '/', '|', '\\'])
        while not job.ready():
            sys.stdout.write(spinner.next())  # write the next character
            sys.stdout.flush()                # flush stdout buffer (actual character display)
            sys.stdout.write('\b')            # erase the last written char
            time.sleep(.1)

        # this causes the exception to bubble up
        (check_results, total_checks) = job.get()
       
        # build summary and notify
        if config.exists():
            event = '{0} had a "{1}" that {2} "{3}" after {4} check{5}'.format(
                    url, check_type,
                    'matched' if check_results else 'did not match',
                    check_value, total_checks,
                    's' if total_checks > 1 else '')

            job = pool.apply_async(tell, (event,))
            click.echo('Telling your channels')
            job.wait()

    except core.TMWCoreException, e:
        click.secho('TMW ERROR: %s' % e.message, fg='red', bold=True)
    except ConnectionError, e:
        click.secho('CONNECTION ERROR: %s' % e.message, fg='red', bold=True)
    except Exception, e:
        click.secho('GENERAL ERROR: %s' % e.message, fg='red', bold=True)

    # shut down the pool
    pool.close()
    pool.join()

    click.echo()
    click.secho('Told you so!', bg='green', fg='white', bold=True)

@cli.command()
@click.option('--force', is_flag=True,
    help='Force configuration (i.e. redo an existing one)')
def configure_notifications(force):
    """Configure notification settings (e.g. smtp/slack settings)"""

    if config.exists():
        if not force:
            click.echo('Config already exists - try again with --force')
            return
        else:
            click.echo('Replacing existing config')

    local_config = {}
    keyring_config = {}
    any_channel = False
    click.secho('## Notification Configuration ##', bg='blue', fg='white', bold=True)
    for channel in channels.keys():
        
        enable = click.prompt('Enable {0} channel? (y/n)'.format(channel), 
            type=bool)
        
        if enable:
            any_channel = True
            local_config[channel] = {}
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
                    local_config[channel][f['name']] = None
                else:
                    local_config[channel][f['name']] = value

            if keyring_config:
                click.echo('Saving sensitive data to keyring')
                for k,v in keyring_config.iteritems():
                    keyring.set_password(config.KEYRING_SVC, k, v)

    if any_channel:
        click.echo('Saving config file {0}'.format(config.CFG_FILE))
        with open(config.CFG_FILE, 'w') as f:
            f.write(json.dumps(local_config, indent=4))
    else:
        click.secho('WARNING: No channels enabled - not writing config', 
                bg='yellow', fg='black')

@cli.command()
def serve():
    """Run the flask server."""
    app.run()

@cli.command()
def debug():
    app.debug = True
    app.run()
