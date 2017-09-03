import flask
from flask import Flask, request
import jinja2
from urllib.parse import urlencode

from .manage import Tracemail, DatabaseError
from .config import load as load_config


app = Flask('tracemail')

jinja_env = jinja2.Environment(
    loader = jinja2.PackageLoader('tracemail', 'templates'),
    autoescape = True,
)


config = load_config('config.toml')
tm = Tracemail(config)


@app.route('/')
def list_aliases():
    error = request.args.get('error', None)
    template = jinja_env.get_template('list.html')
    return template.render(prefix=config.app.prefix, error=error, list=tm.list_aliases())


@app.route('/new', methods=['POST'])
def new_alias():
    error = None
    try:
        tm.new_alias(request.form['alias'], request.form['mailbox'], request.form['purpose'])
    except DatabaseError as e:
        error = str(e)

    return flask.redirect('/' if not error else '/error=' + urlencode(error), code=303)


@app.route('/delete', methods=['POST'])
def delete_alias():
    error = None
    try:
        tm.delete_alias(request.form['alias'])
    except DatabaseError as e:
        error = str(e)

    return flask.redirect('/' if not error else '/error=' + urlencode(error), code=303)
