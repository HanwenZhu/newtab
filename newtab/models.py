import bisect
import datetime

import requests


class Now:

    # TODO, this is only 2019-2020
    # TODO, worry about timezones
    # TODO, what if school on weekends

    # Holidays
    HOLIDAYS = {
        datetime.date(2019, 9, 13): 'Mid-Autumn Festival',
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
        datetime.date(2020, 1, 6): 'Christmas & New Year Holiday',
        datetime.date(2020, 1, 7): 'Christmas & New Year Holiday',
        datetime.date(2020, 1, 8): 'Christmas & New Year Holiday',
        datetime.date(2020, 1, 9): 'Christmas & New Year Holiday',
        datetime.date(2020, 1, 10): 'Christmas & New Year Holiday',
        datetime.date(2020, 4, 3): 'Qingming Festival and Spring Break',
        datetime.date(2020, 4, 4): 'Qingming Festival and Spring Break',
        datetime.date(2020, 4, 5): 'Qingming Festival and Spring Break',
        datetime.date(2020, 4, 6): 'Qingming Festival and Spring Break',
        datetime.date(2020, 4, 7): 'Qingming Festival and Spring Break',
        datetime.date(2020, 4, 8): 'Qingming Festival and Spring Break',
        datetime.date(2020, 4, 9): 'Qingming Festival and Spring Break',
        datetime.date(2020, 4, 10): 'Qingming Festival and Spring Break',
        datetime.date(2020, 4, 11): 'Qingming Festival and Spring Break',
        datetime.date(2020, 4, 12): 'Qingming Festival and Spring Break',
        datetime.date(2020, 5, 1): 'May Labor Day',
    }

    # Special events other than holidays
    EVENTS = {
        datetime.date(2019, 11, 14): 'Parent-Teacher Conference',
        datetime.date(2019, 11, 15): 'Parent-Teacher Conference',
        datetime.date(2019, 11, 22): 'Wierd Staff Day',
    }

    DATE_TO_DAY = {}
    _last_school_day = -1
    for date_ordinal in range(datetime.date(2019, 8, 26).toordinal(),
                              datetime.date(2020, 6, 19).toordinal()):
        date = datetime.date.fromordinal(date_ordinal)
        special = HOLIDAYS.get(date, '') or EVENTS.get(date, '')
        if special:
            DATE_TO_DAY[date] = special
        elif date.weekday() in {5, 6}:
            DATE_TO_DAY[date] = 'Weekend'
        else:
            _last_school_day += 1
            _last_school_day %= 6
            day = ['A', 'B', 'C', 'D', 'E', 'F'][_last_school_day]
            DATE_TO_DAY[date] = 'Day ' + day

    WEEKDAYS = [
        'Monday',
        'Tuesday',
        'Wednesday',
        'Thursday',
        'Friday',
        'Saturday',
        'Sunday',
    ]

    TIMETABLE = {
        'Day A': [0, 1, 2, 3, 4, 5],
        'Day B': [6, 0, 1, 5, 3, 7],
        'Day C': [6, 5, 0, 3, 8, 4],
        'Day D': [2, 5, 0, 4, 1, 6],
        'Day E': [3, 2, 4, 6, 9, 1],
        'Day F': [4, 5, 0, 1, 6, 3],
    }

    CLASSES = [
        ('S406', 'Computer Science'),
        ('2301', 'Mathematics'),
        ('N110', 'Theory of Knowledge'),
        ('S204', 'Economics'),
        ('S303', 'Chinese A'),
        ('N305', 'Physics'),
        ('N204', 'English A'),
        ('N403', 'C4C History'),
        ('N402', 'C4C Politics'),
        ('2301', 'College Counseling'),
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

    def __init__(self):
        now = datetime.datetime.now()
        self.today = self.DATE_TO_DAY[now.date()]
        self.mdHMS = now.strftime('%m%d%H%M%S')
        self.day = self.WEEKDAYS[now.weekday()]

        if self.today.startswith('Day '):
            if self.day == 'Friday':
                schedule = self.FRIDAY_SCHEDULE
            else:
                schedule = self.WEEKDAY_SCHEDULE
            start_times, end_times = list(zip(*schedule))
            next_end = bisect.bisect(end_times, now.time())
            if next_end == len(end_times):
                self.room = ''
                self.activity = 'Afterschool'
            else:
                class_index = self.TIMETABLE[self.today][next_end]
                self.room, self.activity = self.CLASSES[class_index]
                class_time = schedule[next_end]
                self.activity = (f'{class_time[0].strftime("%H:%M")}&ndash;'
                                 f'{class_time[1].strftime("%H:%M")} '
                                 f'{self.activity}')
                next_start = bisect.bisect(start_times, now.time())
                if next_start == next_end:
                    self.activity = f'Next up: {self.activity}'
                self.activity += f', {self.today}'
        else:
            self.room = ''
            self.activity = self.today

    def status(self):
        return {
            'mdHMS': self.mdHMS,
            'day': self.day,
            'room': self.room,
            'activity': self.activity
        }


class Login:

    def __init__(self):
        pass

    def do_encrypt_rc4(self, source, password):
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

    def login(self, username, password):
        rc4key = str(int(datetime.datetime.now().timestamp() * 1000))
        pwd = self.do_encrypt_rc4(password, rc4key)
        params = {
            'opr': 'pwdLogin',
            'userName': username,
            'pwd': pwd,
            'rc4key': rc4key,
            'rememberPwd': '1'
        }
        requests.post('http://1.1.1.3/ac_portal/login.php', data=params)
