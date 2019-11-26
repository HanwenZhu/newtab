import base64
import json
import os
import socket
import subprocess
import sys
import time
import uuid

import requests

import newtab


def google_connectivity(timeout=5):
    try:
        response = requests.head('http://google.com', timeout=timeout)
    except requests.ConnectionError:
        return False
    else:
        return response.elapsed.total_seconds()


def baidu_connectivity(timeout=5):
    try:
        response = requests.head('http://baidu.com', timeout=timeout)
    except requests.ConnectionError:
        return False
    else:
        return response.elapsed.total_seconds()


def ip():
    return socket.gethostbyname(hostname())


def hostname():
    return socket.gethostname()


def mac():
    return ':'.join(f'{byte:02x}'
                    for byte in uuid.getnode().to_bytes(6, 'big'))


def wifi():
    if sys.platform != 'darwin':
        return False  # TODO
    commands = ['networksetup', '-getairportnetwork', 'en0']
    output = subprocess.check_output(commands, shell=False).decode()
    if output.startswith('You are not associated with an AirPort network.\n'):
        return False
    return output.split()[-1]


def login():
    creds_filename = os.path.join(newtab.app.instance_path, 'wifi-creds.json')
    if not os.path.isfile(creds_filename):
        return False
    if wifi() not in {'SJWIRELESS', 'STUWIRELESS'}:
        return False

    with open(creds_filename) as file:
        credentials = json.load(file)
    password = base64.b64decode(credentials['password']).decode()
    rckey = str(int(time.time() * 1000))
    pwd = _do_encrypt_rc4(password, rckey)
    params = {
        'opr': 'pwdLogin',
        'userName': credentials['username'],
        'pwd': pwd,
        'rc4Key': rckey,
        'rememberPwd': '1'
    }
    response = requests.post('http://1.1.1.3/ac_portal/login.php', data=params)
    response.encoding = 'utf-8'
    status = json.loads(response.text.replace("'", '"'))
    logged_in = '用户已在线，不需要再次认证'
    return status.get('success') or status.get('msg') == logged_in


def _do_encrypt_rc4(source, raw_key):
    # Literal line-by-line translation of the original do_encrypt_rc4
    # JavaScript function of the login page
    source = source.strip()

    key = []
    sbox = []
    for i in range(256):
        key.append(ord(raw_key[i % len(raw_key)]))
        sbox.append(i)

    j = 0
    for i in range(256):
        j = (j + sbox[i] + key[i]) % 256
        sbox[i], sbox[j] = sbox[j], sbox[i]

    output = []
    a = b = c = 0
    for i in range(len(source)):
        a = (a + 1) % 256
        b = (b + sbox[a]) % 256
        sbox[a], sbox[b] = sbox[b], sbox[a]
        c = (sbox[a] + sbox[b]) % 256
        out = ord(source[i]) ^ sbox[c]
        out = hex(out).lstrip('0x').rjust(2, '0')
        output.append(out)

    return ''.join(output)
