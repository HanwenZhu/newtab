from flask import jsonify, render_template

import newtab


@newtab.app.route('/')
def index():
    return render_template('index.html')


@newtab.app.route('/status')
def status():
    return jsonify(newtab.clock.status())
