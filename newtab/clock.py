import bisect
import datetime


# TODO, this is only 2019-2020
# TODO, what if school on weekends

SCHOOL_TIMEZONE = datetime.timezone(datetime.timedelta(hours=8))

# Holidays
HOLIDAYS = {
    datetime.date(2019, 9, 13): 'Mid-autumn Festival',
    datetime.date(2019, 9, 28): 'National Holiday',
    datetime.date(2019, 9, 29): 'National Holiday',
    datetime.date(2019, 9, 30): 'National Holiday',
    datetime.date(2019, 10, 1): 'National Holiday',
    datetime.date(2019, 10, 2): 'National Holiday',
    datetime.date(2019, 10, 3): 'National Holiday',
    datetime.date(2019, 10, 4): 'National Holiday',
    datetime.date(2019, 10, 5): 'National Holiday',
    datetime.date(2019, 10, 6): 'National Holiday',
    datetime.date(2019, 10, 7): 'National Holiday',
    datetime.date(2019, 12, 23): 'Christmas, Not Decided',
    datetime.date(2019, 12, 24): 'Christmas, Not Decided',
    datetime.date(2019, 12, 25): 'Christmas, Not Decided',
    datetime.date(2019, 12, 26): 'Christmas & New Year Holiday',
    datetime.date(2019, 12, 27): 'Christmas & New Year Holiday',
    datetime.date(2019, 12, 28): 'Christmas & New Year Holiday',
    datetime.date(2019, 12, 29): 'Christmas & New Year Holiday',
    datetime.date(2019, 12, 30): 'Christmas & New Year Holiday',
    datetime.date(2019, 12, 31): 'Christmas & New Year Holiday',
    datetime.date(2020, 1, 1): 'Christmas & New Year Holiday',
    datetime.date(2020, 1, 2): 'Christmas & New Year Holiday',
    datetime.date(2020, 1, 3): 'Christmas & New Year Holiday',
    datetime.date(2020, 1, 4): 'Christmas & New Year Holiday',
    datetime.date(2020, 1, 5): 'Christmas & New Year Holiday',
    datetime.date(2020, 1, 22): 'Winter Break, Not Decided',
    datetime.date(2020, 1, 23): 'Winter Break',
    datetime.date(2020, 1, 24): 'Winter Break',
    datetime.date(2020, 1, 25): 'Winter Break',
    datetime.date(2020, 1, 26): 'Winter Break',
    datetime.date(2020, 1, 27): 'Winter Break',
    datetime.date(2020, 1, 28): 'Winter Break',
    datetime.date(2020, 1, 29): 'Winter Break',
    datetime.date(2020, 1, 30): 'Winter Break',
    datetime.date(2020, 1, 31): 'Winter Break',
    datetime.date(2020, 2, 1): 'Winter Break',
    datetime.date(2020, 2, 2): 'Winter Break',
    datetime.date(2020, 2, 3): 'Winter Break',
    datetime.date(2020, 2, 4): 'Winter Break',
    datetime.date(2020, 2, 5): 'Winter Break',
    datetime.date(2020, 2, 6): 'Winter Break',
    datetime.date(2020, 2, 7): 'Winter Break',
    datetime.date(2020, 2, 8): 'Winter Break',
    datetime.date(2020, 2, 9): 'Winter Break',
    datetime.date(2020, 2, 10): 'Winter Break',
    datetime.date(2020, 4, 3): 'Qingming Festival',
    datetime.date(2020, 4, 4): 'Qingming Festival',
    datetime.date(2020, 4, 5): 'Qingming Festival',
    datetime.date(2020, 4, 6): 'Qingming Festival',
    datetime.date(2020, 4, 7): 'Qingming Festival',
    datetime.date(2020, 4, 8): 'Qingming Festival',
    datetime.date(2020, 4, 9): 'Qingming Festival',
    datetime.date(2020, 4, 10): 'Qingming Festival',
    datetime.date(2020, 4, 11): 'Qingming Festival',
    datetime.date(2020, 4, 12): 'Qingming Festival',
    datetime.date(2020, 5, 1): 'May Labor Day',
}

# Special events other than holidays
EVENTS = {
    datetime.date(2019, 11, 14): 'Parent–Teacher Conference',
    datetime.date(2019, 11, 15): 'Parent–Teacher Conference',
    datetime.date(2019, 11, 22): 'Wierd Staff Day',
}

DATE_TO_STRING = {}
DATE_IS_SCHOOL = {}
_last_school_day = -1
for _date_ordinal in range(datetime.date(2019, 8, 26).toordinal(),
                           datetime.date(2020, 6, 19).toordinal()):
    _date = datetime.date.fromordinal(_date_ordinal)
    _special = HOLIDAYS.get(_date, '') or EVENTS.get(_date, '')
    if _special:
        DATE_TO_STRING[_date] = _special
        DATE_IS_SCHOOL[_date] = False
    elif _date.weekday() in {5, 6}:
        DATE_TO_STRING[_date] = 'Weekend'
        DATE_IS_SCHOOL[_date] = False
    else:
        _last_school_day += 1
        _last_school_day %= 6
        _day = ['A', 'B', 'C', 'D', 'E', 'F'][_last_school_day]
        DATE_TO_STRING[_date] = _day
        DATE_IS_SCHOOL[_date] = True

TIMETABLE = {
    'A': [0, 1, 2, 3, 4, 5],
    'B': [6, 0, 1, 5, 3, 7],
    'C': [6, 5, 0, 3, 8, 4],
    'D': [2, 5, 0, 4, 1, 6],
    'E': [3, 2, 4, 6, 9, 1],
    'F': [4, 5, 0, 1, 6, 3],
}

CLASSES = [
    'Computer',
    'Math',
    'Knowledge',
    'Economics',
    'Chinese',
    'Physics',
    'English',
    'History',
    'Politics',
    'College',
]

WEEKDAY_SCHEDULE = [
    (datetime.time(8, 0), datetime.time(9, 0)),
    (datetime.time(9, 5), datetime.time(10, 5)),
    (datetime.time(10, 20), datetime.time(11, 20)),
    (datetime.time(11, 25), datetime.time(12, 25)),
    (datetime.time(13, 40), datetime.time(14, 40)),
    (datetime.time(14, 45), datetime.time(15, 45)),
]

FRIDAY_SCHEDULE = [
    (datetime.time(8, 0), datetime.time(8, 55)),
    (datetime.time(9, 0), datetime.time(9, 55)),
    (datetime.time(10, 10), datetime.time(11, 5)),
    (datetime.time(11, 10), datetime.time(12, 5)),
    (datetime.time(13, 5), datetime.time(14, 0)),
    (datetime.time(14, 5), datetime.time(15, 0)),
]


def strftime(directive):
    now = datetime.datetime.now()
    return now.strftime(directive)


def school():
    now = datetime.datetime.now(tz=SCHOOL_TIMEZONE)
    date = now.date()
    today = DATE_TO_STRING[date]

    if DATE_IS_SCHOOL[date]:
        classes = [CLASSES[class_index] for class_index in TIMETABLE[today]]

        if now.weekday() == 4:
            schedule = FRIDAY_SCHEDULE
        else:
            schedule = WEEKDAY_SCHEDULE
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
            'today': today,
            'school': True,
            'classes': classes,
            'classIndex': next_end,
            'started': next_start != next_end,
            'progress': progress,
        }

    else:
        return {
            'today': today,
            'school': False
        }
