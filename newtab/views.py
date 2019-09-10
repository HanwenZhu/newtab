from flask import jsonify, render_template

from newtab import app
from newtab.models import Now


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/status')
def status():
    # TODO, put this to another file
    return jsonify(Now().status())
