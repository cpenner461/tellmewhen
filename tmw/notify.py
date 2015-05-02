
from collections import defaultdict
import os
import pwd
import smtplib

import keyring

from config import KEYRING_SVC, load_config

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


def notify(event):
    """Notify of an event"""

    for channel in load_config():
        if channel == 'smtp':
            print('smtp notify')
            smtp_send(event, load_config()['smtp'])
        
        if channel == 'slack':
            print('no slack yet')

def smtp_send(event, config):
    """Send a notification via SMTP"""

    from_addr = config.get('sender')
    to_addr = config.get('recipients')
    
    msg = ('From: {0}\r\nTo: {1}\r\nSubject: [tellmewhen]\r\n\r\n'.format(
           from_addr, to_addr))
    msg = msg + event

    s = smtplib.SMTP_SSL(config.get('server'), config.get('port'))
    s.login(config.get('username'), keyring.get_password(KEYRING_SVC, 'smtp:password'))
    s.sendmail(from_addr, to_addr, msg)
    s.quit()

'''
# having problems getting the email libs to work with the multipart stuff
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
def _smtp_send(event, config):
    """Send a notification via SMTP"""
    
    msg = MIMEMultipart('alternative')

    from_addr = config.get('sender')
    to_addr = config.get('recipients', '').split(',')
    msg['From'] = from_addr
    msg['To'] = to_addr
    msg['Subject'] = '[tellmewhen]'
    text = event
    html = '<html><head></head><body><h1>tellmewhen</h1><p>{0}</p></body></html>'.format(
        event)

    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')

    msg.attach(part1)
    msg.attach(part2)

    import pdb; pdb.set_trace()
    print("msg:\n%s" % msg.as_string())

    s = smtplib.SMTP(config.get('server'))
    s.sendmail(from_addr, to_addr, msg.as_string())
    s.quit()
'''
