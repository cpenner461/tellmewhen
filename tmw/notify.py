'''
Handle all notifications/telling for when events have met the specified
criteria.
'''

from collections import defaultdict
import os
import pwd
import smtplib

import keyring

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
        { 'name': 'username', 'type': unicode, 'default': _curr_user(), },
        { 'name': 'password', 'type': unicode, 'default': None, 'hide_input': True, },
        { 'name': 'channel', 'type': unicode, 'default': None, },
    ]
}
channels = defaultdict(list)
for n in (smtp_config, slack_config):
    channels[n['name']] = n

def tell(event):
    """Tell all configured channels about an event"""

    for channel in load_config():
        if channel == 'smtp':
            print('[smtp] tell')
            tell_smtp(event, load_config()['smtp'])
        
        if channel == 'slack':
            print('[slack] tell')
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
    print("NO SLACK!")

