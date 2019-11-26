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


@newtab.app.route('/wifi/wifi')
def wifi_wifi():
    return jsonify(newtab.wifi.wifi())


@newtab.app.route('/wifi/ip')
def wifi_ip():
    return jsonify(newtab.wifi.ip())


@newtab.app.route('/wifi/hostname')
def wifi_hostname():
    return jsonify(newtab.wifi.hostname())


@newtab.app.route('/wifi/mac')
def wifi_mac():
    return jsonify(newtab.wifi.mac())


@newtab.app.route('/wifi/google')
def wifi_google():
    return jsonify(newtab.wifi.google_connectivity())


@newtab.app.route('/wifi/baidu')
def wifi_baidu():
    return jsonify(newtab.wifi.baidu_connectivity())


@newtab.app.route('/wifi/login')
def wifi_login():
    return jsonify(newtab.wifi.login())
