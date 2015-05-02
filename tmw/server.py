from flask import Flask
from flask import render_template, request, redirect
import core
app = Flask(__name__)

@app.route('/')
@app.route('/index.html', alias=True)
def index():
    return render_template('index.html')

@app.route('/hello')
def hello():
    return render_template('hello.html')

@app.route('/tellme', methods = ['POST'])
def tellme():

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
