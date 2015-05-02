
import json
import os

CFG_FILE = os.path.expanduser("~/.tellmewhen")
KEYRING_SVC = "tellmewhen"

def _exists():
    """Verify if a config file exists"""
    return os.path.exists(CFG_FILE)

def load_config():
    """Load the entire config"""
    if _exists():
        return json.loads(open(CFG_FILE, 'r').read())

    return {}

def load_channel_config(channel):
    """Load the config file"""
    return load_config().get(channel, {})
