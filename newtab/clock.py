import bisect
import collections
import datetime
import json
import os

import newtab


_Date = collections.namedtuple('_Date',
                               ['description', 'is_school', 'timetable_index'])


def _parse_date(string):
    return datetime.datetime.strptime(string, '%Y-%m-%d').date()


def _parse_dates(key):
    return {
        _parse_date(date): name for date, name in _config[key].items()
    }


def _parse_time(string):
    return datetime.datetime.strptime(string, '%H:%M').time()


def _parse_times(key):
    return [
        (_parse_time(start), _parse_time(end)) for start, end in _config[key]
    ]


_config_file = os.path.join(newtab.app.instance_path, 'clock.json')
if not os.path.isfile(_config_file):
    raise FileNotFoundError('instance/clock.json not found')

with open(_config_file, encoding='utf-8') as _file:
    _config = json.load(_file)

_user_config_file = os.path.join(newtab.app.instance_path, 'clock-user.json')
if os.path.isfile(_user_config_file):
    with open(_user_config_file, encoding='utf-8') as _file:
        _config.update(json.load(_file))


_school_timezone = datetime.timezone(datetime.timedelta(
    hours=_config['school_timezone']
))

# Holidays
_holidays = _parse_dates('holidays')
# Special events other than holidays
_events = _parse_dates('events')
# Make-up school days
_makeups = _parse_dates('makeups')

_rotation = _config['rotation']
if _rotation:
    _rotation_days = _config['rotation_days']
_timetable = _config['timetable']
_classes = _config['classes']

_weekday_schedule = _parse_times('weekday_schedule')
_friday_schedule = _parse_times('friday_schedule')

_start_date = _parse_date(_config['start_date'])
_end_date = _parse_date(_config['end_date'])

_dates = {}
if _rotation:
    _rotation_index = 0
for _date_ordinal in range(_start_date.toordinal(), _end_date.toordinal()):
    _date = datetime.date.fromordinal(_date_ordinal)
    _special = _holidays.get(_date, '') or _events.get(_date, '')
    if _special:
        _dates[_date] = _Date(description=_special,
                              is_school=False,
                              timetable_index=None)
    elif _date.weekday() in {5, 6} and _date not in _makeups:
        _dates[_date] = _Date(description='Weekend',
                              is_school=False,
                              timetable_index=None)
    elif _rotation:
        _dates[_date] = _Date(description=_rotation_days[_rotation_index],
                              is_school=True,
                              timetable_index=_rotation_index)
        _rotation_index += 1
        _rotation_index %= len(_rotation_days)
    elif _date in _makeups:
        _dates[_date] = _Date(description='',
                              is_school=True,
                              timetable_index=_makeups[_date])
    else:
        _dates[_date] = _Date(description='',
                              is_school=True,
                              timetable_index=_date.weekday())


def strftime(directive):
    now = datetime.datetime.now()
    try:
        return now.strftime(directive)
    except ValueError:
        return now.strftime(directive.replace('%-', '%#'))


def school():
    now = datetime.datetime.now(tz=_school_timezone)
    date = now.date()
    today = _dates[date]

    if today.is_school:
        classes = [_classes[class_index]
                   for class_index in _timetable[today.timetable_index]]

        if now.weekday() == 4:
            schedule = _friday_schedule
        else:
            schedule = _weekday_schedule
        start_times, end_times = list(zip(*schedule))
        next_end = bisect.bisect(end_times, now.time())
        next_start = bisect.bisect(start_times, now.time())

        if next_start == next_end == 0:
            start_time = datetime.time.min
            end_time = start_times[next_start]
        elif next_start == next_end == len(schedule):
            start_time = end_times[next_end - 1]
            end_time = datetime.time.max
        elif next_start == next_end:
            start_time = end_times[next_end - 1]
            end_time = start_times[next_start]
        else:
            start_time = start_times[next_start - 1]
            end_time = end_times[next_end]

        start = datetime.datetime.combine(now, start_time)
        end = datetime.datetime.combine(now, end_time)
        now_naive = now.replace(tzinfo=None)
        progress = (now_naive - start) / (end - start)

        return {
            'today': today.description,
            'school': True,
            'classes': classes,
            'classIndex': next_end,
            'started': next_start != next_end,
            'progress': progress,
        }

    else:
        return {
            'today': today.description,
            'school': False
        }
