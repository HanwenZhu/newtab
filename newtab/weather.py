import multiprocessing
import re
import time

import requests


# A very good API
URL = 'http://wttr.in/?format=%22%t+%c%22'
# r'..?' since a unicode emoji might take up to two bytes
WTTR_IN_RE = re.compile(r'"(\+|-)[0-9]+°C ..?"\n')
REFRESH_RATE = 1800


def _update_weather(status_queue):
    while True:
        try:
            response = requests.get(URL, allow_redirects=False)
        except requests.exceptions.ConnectionError:
            time.sleep(120)
            continue
        else:
            response.encoding = 'utf-8'
            text = response.text
            if response.status_code == 200 and WTTR_IN_RE.fullmatch(text):
                status_queue.get()
                status_queue.put(
                    # If the temperature starts with a plus sign
                    text.lstrip('"+').rstrip('"\n').replace('C', '')
                )
            time.sleep(REFRESH_RATE)


_status_queue = multiprocessing.SimpleQueue()
_status_queue.put('')


def status():
    weather_status = _status_queue.get()
    _status_queue.put(weather_status)
    return weather_status


multiprocessing.Process(target=_update_weather, args=(_status_queue,)).start()
