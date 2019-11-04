from flask import jsonify, render_template

import newtab


@newtab.app.route('/')
def index():
    return render_template('index.html')


@newtab.app.route('/clock')
def clock():
    return jsonify(newtab.clock.status())


@newtab.app.route('/weather')
def weather():
    return jsonify(newtab.weather.status())
