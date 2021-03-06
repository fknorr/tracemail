import flask
from flask import Flask, request
import jinja2
from urllib.parse import urlencode

from .manage import Tracemail, DatabaseError
from .config import load as load_config


config = load_config('config.toml')

app = Flask('tracemail')
app.config['APPLICATION_ROOT'] = config.app.prefix

jinja_env = jinja2.Environment(
    loader = jinja2.PackageLoader('tracemail', 'templates'),
    autoescape = True,
)

tm = Tracemail(config)


@app.route('/')
def list_aliases():
    error = request.args.get('error', None)
    template = jinja_env.get_template('list.html')
    return template.render(prefix=config.app.prefix, error=error, list=tm.list_aliases())


def redirect_to_list_page(error=None):
    query = '?' + urlencode({ 'error' : error}) if error else ''
    return flask.redirect(config.app.prefix + '/' + query, code=303)


@app.route('/new', methods=['POST'])
def new_alias():
    error = None
    try:
        tm.new_alias(request.form['alias'], request.form['mailbox'], request.form['purpose'])
    except DatabaseError as e:
        error = str(e)

    return redirect_to_list_page(error)


@app.route('/delete', methods=['POST'])
def delete_alias():
    error = None
    try:
        tm.delete_alias(request.form['alias'])
    except DatabaseError as e:
        error = str(e)

    return redirect_to_list_page(error)
