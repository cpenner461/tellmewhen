
import json
import os

# some constants
NUM_PROCESSES = 3

# most of this is notification config 
CFG_FILE = os.path.expanduser("~/.tellmewhen")
KEYRING_SVC = "tellmewhen"

def exists():
    """Verify if a config file exists"""
    return os.path.exists(CFG_FILE)

def load_config():
    """Load the entire config"""
    if exists():
        return json.loads(open(CFG_FILE, 'r').read())

    return {}

def write_config(config):
    """Saves the config"""
    with open(CFG_FILE, 'w') as f:
        f.write(json.dumps(config, indent=4))

def load_channel_config(channel):
    """Load the config file"""
    return load_config().get(channel, {})

