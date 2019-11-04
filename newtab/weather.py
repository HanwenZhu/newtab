import multiprocessing
import time

import requests


# A very good API
URL = 'http://wttr.in/?format=%22%t+%c%22'
REFRESH_RATE = 1800


def _update_weather(status_queue):
    while True:
        try:
            response = requests.get(URL)
        except requests.exceptions.ConnectionError:
            pass
        else:
            response.encoding = 'utf-8'
            status_queue.get()
            status_queue.put(
                # If the temperature starts with a plus sign
                response.text.lstrip('"+').rstrip('"\n').replace('C', '')
            )
        finally:
            time.sleep(REFRESH_RATE)


_status_queue = multiprocessing.SimpleQueue()
_status_queue.put('')


def status():
    weather_status = _status_queue.get()
    _status_queue.put(weather_status)
    return weather_status


multiprocessing.Process(target=_update_weather, args=(_status_queue,)).start()
