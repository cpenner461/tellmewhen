'''
Handle all notifications/telling for when events have met the specified
criteria.
'''

from collections import defaultdict
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import json
import os
import pwd
import smtplib

from jinja2 import Environment, PackageLoader
import keyring
import requests

# TODO this is a Bad Idea
# https://urllib3.readthedocs.org/en/latest/security.html#insecureplatformwarning
# https://urllib3.readthedocs.org/en/latest/security.html
from requests.packages import urllib3
urllib3.disable_warnings()

from tmw.config import SUBJECT, KEYRING_SVC, load_config

def _curr_user():
    uid = os.geteuid()
    return pwd.getpwuid(uid)[0]

smtp_config = {
    'name': 'smtp',
    'fields': [
        { 'name': 'server', 'type': str, 'default': 'localhost', },
        { 'name': 'port', 'type': int, 'default': 465, },
        { 'name': 'username', 'type': str, 'default': _curr_user(), },
        { 'name': 'password', 'type': str, 'default': None, 'hide_input': True, },
        { 'name': 'sender', 'type': str, 'default': None, },
        { 'name': 'recipients', 'type': str, 'default': None, },
    ]
}
slack_config = {
    'name': 'slack',
    'fields': [
        { 'name': 'webhook_url', 'type': str, 'default': None, },
        { 'name': 'channel', 'type': str, 'default': '#tellmewhen', },
    ]
}
channels = defaultdict(list)
for n in (smtp_config, slack_config):
    channels[n['name']] = n

def _event_text(event):
    '''Convert an event dict to a string'''

    return '{0} had a "{1}" that {2} "{3}" after {4} check{5}'.format(
            event['url'], 
            event['check_type'],
            'matched' if event['check_results'] else 'did not match',
            event['check_value'], 
            event['total_checks'],
            's' if event['total_checks'] > 1 else '')

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
  
    msg = MIMEMultipart('alternative')
    msg['Subject'] = '{0} ({1}) {2}'.format(SUBJECT, 
        '+' if event['check_results'] else '-',
        event['url'],
        )
    msg['From'] = from_addr
    msg['To'] = to_addr

    text = '%s' % event
    
    env = Environment(loader=PackageLoader('tmw', 'templates'))
    html_template = env.get_template('email-notification.html') 

    html = html_template.render(
        url=event['url'],
        check_type=event['check_type'],
        check_results=event['check_results'],
        check_value=event['check_value'],
        total_checks=event['total_checks'],
    )

    msg.attach(MIMEText(text, 'plain'))
    msg.attach(MIMEText(html, 'html'))

    s = smtplib.SMTP_SSL(config.get('server'), config.get('port'))
    s.login(config.get('username'), keyring.get_password(KEYRING_SVC, 'smtp:password'))
    s.sendmail(from_addr, to_addr, msg.as_string())
    s.quit()

def tell_slack(event, config):
    """Tell slack about an event"""
    
    slack_url = config.get("webhook_url")

    payload = {
        "channel": config.get("channel", "#general"),
        "username": "webhookbot",
        "text": _event_text(event),
    }

    response = requests.post(slack_url, data=json.dumps(payload), verify=False)

