'''
Handle all notifications/telling for when events have met the specified
criteria.
'''

from collections import defaultdict
import json
import os
import pwd
import smtplib

import keyring
import requests

# TODO this is a Bad Idea
# https://urllib3.readthedocs.org/en/latest/security.html#insecureplatformwarning
# https://urllib3.readthedocs.org/en/latest/security.html
from requests.packages import urllib3
urllib3.disable_warnings()

from tmw.config import KEYRING_SVC, load_config

def _curr_user():
    uid = os.geteuid()
    return pwd.getpwuid(uid)[0]

smtp_config = {
    'name': 'smtp',
    'fields': [
        { 'name': 'server', 'type': unicode, 'default': 'localhost', },
        { 'name': 'port', 'type': int, 'default': 465, },
        { 'name': 'username', 'type': unicode, 'default': _curr_user(), },
        { 'name': 'password', 'type': unicode, 'default': None, 'hide_input': True, },
        { 'name': 'sender', 'type': unicode, 'default': None, },
        { 'name': 'recipients', 'type': unicode, 'default': None, },
    ]
}
slack_config = {
    'name': 'slack',
    'fields': [
        { 'name': 'webhook_url', 'type': unicode, 'default': None, },
        { 'name': 'channel', 'type': unicode, 'default': '#tellmewhen', },
    ]
}
channels = defaultdict(list)
for n in (smtp_config, slack_config):
    channels[n['name']] = n

def tell(event):
    """Tell all configured channels about an event"""

    for channel in load_config():
        if channel == 'smtp':
            print('  [smtp] tell')
            tell_smtp(event, load_config()['smtp'])
        
        if channel == 'slack':
            print('  [slack] tell')
            tell_slack(event, load_config()['slack'])

def tell_smtp(event, config):
    """Tell smtp about an event"""

    from_addr = config.get('sender')
    to_addr = config.get('recipients')
    
    msg = ('From: {0}\r\nTo: {1}\r\nSubject: [tellmewhen]\r\n\r\n'.format(
           from_addr, to_addr))
    msg = msg + event

    s = smtplib.SMTP_SSL(config.get('server'), config.get('port'))
    s.login(config.get('username'), keyring.get_password(KEYRING_SVC, 'smtp:password'))
    s.sendmail(from_addr, to_addr, msg)
    s.quit()

def tell_slack(event, config):
    """Tell slack about an event"""
    
    slack_channel = config.get("channel")
    slack_url = config.get("webhook_url")

    payload = {
        "channel": config.get("channel", "#general"),
        "username": "webhookbot",
        "text": event,
        "icon-emoji": "alias:squirrel",
    }

    response = requests.post(slack_url, data=json.dumps(payload), verify=False)

