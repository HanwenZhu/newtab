import re
import threading
import time

import requests

import newtab


# A very good API
URL = 'http://wttr.in/?m&format=%t+%c'
# r'..?' since a unicode emoji might take up to two bytes
WTTR_IN_RE = re.compile(r'(\+|-)[0-9]+°C ..?\s*')
REFRESH_RATE = 1800


_initialized = False


def _update_weather():
    global _weather_status
    try:
        response = requests.get(URL, allow_redirects=False, timeout=10)
    except requests.exceptions.RequestException as error:
        newtab.app.logger.warn(f'Could not update weather: {error}')
        return False
    else:
        response.encoding = 'utf-8'
        text = response.text
        if response.status_code == 200 and WTTR_IN_RE.fullmatch(text):
            # If the temperature starts with a plus sign
            _weather_status = text.lstrip('+').rstrip().replace('C', '')
            newtab.app.logger.info(f'Weather status: {_weather_status}')
            return True
        else:
            newtab.app.logger.warn('Could not update weather: '
                                   f'wttr.in returned {response}: '
                                   f'{response.text}')
            return False


def _background_update():
    while True:
        if _update_weather():
            time.sleep(REFRESH_RATE)
        else:
            time.sleep(120)


_weather_status = ''
_process = threading.Thread(target=_background_update)


def status(check=True):
    global _initialized
    if not _initialized:
        _process.start()
        _initialized = True

    if not check or _weather_status:
        return _weather_status
    else:
        _update_weather()
        return status(check=False)
