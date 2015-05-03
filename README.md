## Overview
Use of [virtualenv]() is highly recommended.  You may also want to use 
[virtualenvwrapper]() to simplify management of your virtualenvs.  

For regular use with vanilla `virtualenv` install like this from the root
directory of the Git repo:
```bash
virtualenv tmw 
. tmw/bin/activate
pip install .
```

For development use with vanilla `virtualenv` install like this from the root
directory of the Git repo:

```bash
virtualenv tmw 
. tmw/bin/activate
pip install --editable .
```

Either way, you can simply run the script to see how to use it:

```bash
tmw
```

The subcommand ``tmw web serve`` will start the web server.

If you want better errors from the server when things fail, use the command ``tmw web debug``.


## Development

For now, we're adding [Flask]() commands in ``tmw/server.py`` and adding [Click]()
commands in ``tmw/cli.py``. A new [Click]() command must have the decorator 
``@cli.command()`` on it.

[Click]: http://click.pocoo.org/4/
[Flask]: http://flask.pocoo.org/docs/0.10/
[virtualenv]: https://pypi.python.org/pypi/virtualenv
[virtualenvwrapper]: http://virtualenvwrapper.readthedocs.org

