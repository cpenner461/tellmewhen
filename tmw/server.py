'''
Built-in web server using Flask.  Should mirror functionality offered by the
cli.
'''

from flask import Flask
from flask import render_template, request

import tmw.config as config
import tmw.core as core

from multiprocessing import Pool

app = Flask(__name__)

pool = Pool(processes=2)
jobs = []

@app.route('/', methods = ["POST", "GET"])
def index():
    '''The main landing page and UI for tmw'''

    if request.method == "GET":
        return render_template('index.html')
    else:
        url = request.form.get('url')
        freq = request.form.get('frequency')
        num_checks = request.form.get('num_checks')
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

        jobs.append({ 'url': url, 'value': value, 'status': "pending" })
        return render_template('index.html', jobs=jobs)


@app.route('/hello')
def hello():
    '''Simple page useful for testing/validating your tmw setup'''
    return render_template('hello.html')

@app.route('/settings', methods = ["POST", "GET"])
def settings():
    '''Settings page'''

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

