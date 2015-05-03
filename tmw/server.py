from flask import Flask
from flask import render_template, request, redirect
import config
import core
app = Flask(__name__)

@app.route('/', methods = ["POST", "GET"])
def index():
    if request.method == "GET":
        return render_template('index.html')
    else:
        url = request.form.get('url')
        type = request.form.get('check_type')
        value = None
        if type == 'status_code':
            value = request.form.get('status_code')
        elif type == 'string_match' or type == 'regex_match':
            value = request.form.get('string_match')

        status = core.check_once(url, type, value)

        event_list = [
            { 'url': url, 'check_type': type, 'value': value, 'status': status  }
        ]

        return render_template('index.html', events=event_list)


@app.route('/hello')
def hello():
    return render_template('hello.html')

@app.route('/settings', methods = ["POST", "GET"])
def settings():

    if request.method == "POST":
        f = request.form

        conf = config.load_config()
        _set_config_param(conf, 'smtp', 'username', f)
        _set_config_param(conf, 'smtp', 'sender', f)
        _set_config_param(conf, 'smtp', 'recipients', f)
        _set_config_param(conf, 'smtp', 'server', f)
        _set_config_param(conf, 'smtp', 'port', f, number = True)
        _set_config_param(conf, 'slack', 'username', f)
        _set_config_param(conf, 'slack', 'channel', f, prefix = "#")

        config.write_config(conf)

    return render_template('settings.html')

def _set_config_param(conf, service, param, form, number = False, prefix = ""):
    if not conf.get(service):
        conf[service] = {}
    key = '%s-%s' % (service, param)
    if not conf[service].get(key):
        conf[service][key] = None
    value = form.get(key)
    if value:
        value = prefix + value
    if number and value:
        value = int(value)
    conf[service][key] = value if value else conf[service][key]

