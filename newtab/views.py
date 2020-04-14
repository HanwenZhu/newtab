from flask import jsonify, redirect, url_for, abort, render_template

import newtab
from newtab import app


@app.route('/')
def index():
    return render_template('index.html', theme=app.config.get('THEME'))


@app.route('/theme')
def get_theme():
    return app.config.get('THEME')


@app.route('/theme/<theme>')
def set_theme(theme):
    if theme in app.config.get('THEMES'):
        app.config.update(THEME=theme)
        return redirect(url_for('index'))
    else:
        abort(400)


@app.route('/clock/strftime/<directive>')
def clock_strftime(directive):
    return jsonify(newtab.clock.strftime(directive))


@app.route('/clock/school')
def clock_school():
    return jsonify(newtab.clock.school())


@app.route('/weather')
def weather():
    return jsonify(newtab.weather.status())


@app.route('/wifi/wifi')
def wifi_wifi():
    return jsonify(newtab.wifi.wifi())


@app.route('/wifi/ip')
def wifi_ip():
    return jsonify(newtab.wifi.ip())


@app.route('/wifi/hostname')
def wifi_hostname():
    return jsonify(newtab.wifi.hostname())


@app.route('/wifi/mac')
def wifi_mac():
    return jsonify(newtab.wifi.mac())


@app.route('/wifi/google')
def wifi_google():
    return jsonify(newtab.wifi.google_connectivity())


@app.route('/wifi/baidu')
def wifi_baidu():
    return jsonify(newtab.wifi.baidu_connectivity())


@app.route('/wifi/login')
def wifi_login():
    return jsonify(newtab.wifi.login())
