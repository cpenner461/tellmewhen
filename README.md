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

For now, we're adding flask commands in ``server.py`` and adding click commands in ``tellmewhen.py``. This should probably be restructured -- please update this README when you do that. A new click command must have the decorator ``@cli.command()`` on it.

Click: http://click.pocoo.org/4/
Flask: http://flask.pocoo.org/docs/0.10/



