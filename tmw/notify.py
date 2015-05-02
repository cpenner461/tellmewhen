
from collections import defaultdict
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import pwd
import smtplib

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
        { 'name': 'recipients', 'type': unicode, 'default': None, },
    ]
}
notification_types = defaultdict(list)
for n in (smtp_config, ):
    notification_types[n['name']] = n

# TODO this is just a sample from python code right now 

'''
# me == my email address
# you == recipient's email address
me = "my@email.com"
you = "your@email.com"

# Create message container - the correct MIME type is multipart/alternative.
msg = MIMEMultipart('alternative')
msg['Subject'] = "Link"
msg['From'] = me
msg['To'] = you

# Create the body of the message (a plain-text and an HTML version).
text = "Hi!\nHow are you?\nHere is the link you wanted:\nhttps://www.python.org"
html = """\
<html>
  <head></head>
  <body>
    <p>Hi!<br>
       How are you?<br>
       Here is the <a href="https://www.python.org">link</a> you wanted.
    </p>
  </body>
</html>
"""

# Record the MIME types of both parts - text/plain and text/html.
part1 = MIMEText(text, 'plain')
part2 = MIMEText(html, 'html')

# Attach parts into message container.
# According to RFC 2046, the last part of a multipart message, in this case
# the HTML message, is best and preferred.
msg.attach(part1)
msg.attach(part2)

# Send the message via local SMTP server.
s = smtplib.SMTP('localhost')
# sendmail function takes 3 arguments: sender's address, recipient's address
# and message to send - here it is sent as one string.
s.sendmail(me, you, msg.as_string())
s.quit()
'''
