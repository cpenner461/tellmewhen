## Overview
Install with:

```bash
virtualenv venv
. venv/bin/activate
pip install --editable .
```

Now, you can simply run the script:

```bash
tmw
```

The subcommand ``tmw serve`` will start the web server.


## Development

For now, we're adding flask commands in ``tmw/server.py`` and adding click commands in ``tmw/cli.py``. A new click command must have the decorator ``@cli.command()`` on it.

Click: http://click.pocoo.org/4/
Flask: http://flask.pocoo.org/docs/0.10/



