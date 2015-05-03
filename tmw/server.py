'''
Built-in web server using Flask.  Should mirror functionality offered by the
cli.
'''

from flask import Flask
from flask import render_template, request, session
from flask.ext.session import Session

import tmw.config as config
import tmw.core as core

import json
from uuid import uuid4
from multiprocessing import Pool

app = Flask(__name__)

pool = Pool(processes=2)
jobs = []

@app.route('/', methods = ["POST", "GET"])
def index():
    '''The main landing page and UI for tmw'''

    if request.method == "GET":
        return render_template('index.html', jobs=jobs)
    else:
        url = request.form.get('url')
        freq = int(request.form.get('frequency'))
        num_checks = int(request.form.get('num_checks'))
        check_type = request.form.get('check_type')

        value = None
        if check_type == 'status_code':
            value = request.form.get('status_code')
        elif check_type == 'string_match' or check_type == 'regex_match':
            value = request.form.get('string_match')

        check_results = None
        total_checks = None
        index = None

        def _handle_results(results):
            (check_results, total_checks, index) = results
            jobs[index]['status'] = "success" if check_results else "failure"

        job = pool.apply_async(
            core.check_until,
            (url, check_type, value, freq, num_checks, len(jobs)),
            callback=_handle_results
        )

        jobs.append({ 'url': url, 'value': value, 'status': 'pending' })
        return render_template('index.html', jobs=jobs, success=True)

@app.route('/_job_status')
def _job_status():
    return json.dumps(jobs)

@app.route('/hello')
def hello():
    '''Simple page useful for testing/validating your tmw setup'''
    return render_template('hello.html')

@app.route('/settings', methods = ["POST", "GET"])
def settings():
    '''Settings page'''

    status = None
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
        settings = config
        status = "success"
    else:
        conf = config.load_config()

        settings = {}

        settings['smtp-username'] = _get_config_param(conf, 'smtp', 'username')
        settings['smtp-sender'] = _get_config_param(conf, 'smtp', 'sender')
        settings['smtp-recipients'] = _get_config_param(conf, 'smtp', 'recipients')
        settings['smtp-server'] = _get_config_param(conf, 'smtp', 'server')
        settings['smtp-port'] = _get_config_param(conf, 'smtp', 'port')

        settings['slack-username'] = _get_config_param(conf, 'slack', 'username')
        settings['slack-channel'] = _get_config_param(conf, 'slack', 'channel')

    return render_template('settings.html', status=status, settings=settings)

def _set_config_param(conf, service, param, form, number = False, prefix = ""):
    if not conf.get(service):
        conf[service] = {}
    if not conf[service].get(param):
        conf[service][param] = None
    value = form.get('%s-%s' % (service, param))
    if value:
        value = prefix + value
    if number and value:
        value = int(value)
    conf[service][param] = value if value else conf[service][param]

def _get_config_param(conf, service, param):
    if not conf.get(service):
        conf[service] = {}
    if not conf[service].get(param):
        conf[service][param] = None
    return conf[service][param]

@app.before_request
def csrf_protect():
    if request.method == "POST":
        token = session.pop('_csrf_token', None)
        if not token or unicode(token) != request.form.get('_csrf_token'):
            abort(403)

def _generate_csrf_token():
    if '_csrf_token' not in session:
        session['_csrf_token'] = uuid4()
    return session['_csrf_token']

app.jinja_env.globals['csrf_token'] = _generate_csrf_token

#Remove this later

@app.route('/email-notification')
def the_path():
   return render_template('email-notification.html')
