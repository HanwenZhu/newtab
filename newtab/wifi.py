import time

import requests


def _do_encrypt_rc4(source, password):
    source = source.strip()

    key = []
    sbox = []
    for i in range(256):
        key.append(ord(password[i % len(password)]))
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


def login(username, password):
    rc4key = str(int(time.time() * 1000))
    pwd = _do_encrypt_rc4(password, rc4key)
    params = {
        'opr': 'pwdLogin',
        'userName': username,
        'pwd': pwd,
        'rc4key': rc4key,
        'rememberPwd': '1'
    }
    requests.post('http://1.1.1.3/ac_portal/login.php', data=params)
