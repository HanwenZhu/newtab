import multiprocessing
import re
import time

import requests

import newtab


# A very good API
URL = 'http://wttr.in/?format=%t+%c'
# r'..?' since a unicode emoji might take up to two bytes
WTTR_IN_RE = re.compile(r'(\+|-)[0-9]+°C ..?\n')
REFRESH_RATE = 1800


_initialized = False


def _update_weather():
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
            weather_status = text.lstrip('+').rstrip('\n').replace('C', '')
            _status_queue.get()
            _status_queue.put(weather_status)
            newtab.app.logger.info(f'Weather status: {weather_status}')
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


_status_queue = multiprocessing.SimpleQueue()
_status_queue.put('')

_process = multiprocessing.Process(target=_background_update)


def status(check=True):
    global _initialized
    if not _initialized:
        _process.start()
        _initialized = True

    weather_status = _status_queue.get()
    _status_queue.put(weather_status)
    if not check or weather_status:
        return weather_status
    else:
        _update_weather()
        return status(check=False)
