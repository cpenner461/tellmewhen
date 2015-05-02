
from collections import defaultdict
import os
import smtplib

import keyring
KEYRING_SVC = "tellmewhen"

smtp_config = {
    'name': 'smtp',
    'fields': [
        { 'name': 'server', 'type': unicode, 'default': 'localhost', },
        { 'name': 'port', 'type': int, 'default': 465, },
        { 'name': 'username', 'type': unicode, 'default': os.getlogin(), },
        { 'name': 'password', 'type': unicode, 'default': None, 'hide_input': True, },
        { 'name': 'sender', 'type': unicode, 'default': None, },
        { 'name': 'recipients', 'type': unicode, 'default': None, },

    ]
}
notification_types = defaultdict(list)
for n in (smtp_config, ):
    notification_types[n['name']] = n

def smtp_send(event, config):
    """Send a notification via SMTP"""

    from_addr = config.get('sender')
    to_addr = config.get('recipients')
    
    msg = ('From: {0}\r\nTo: {1}\r\nSubject: [tellmewhen]\r\n\r\n'.format(
           from_addr, to_addr))
    msg = msg + event

    s = smtplib.SMTP_SSL(config.get('server'), config.get('port'))
    s.login(config.get('username'), keyring.get_password(KEYRING_SVC, 'password'))
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
