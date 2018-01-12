import calendar
from datetime import datetime
import re


def convert_event_to_new_format(event):
    date_time = datetime.strptime(event['timestamp'], '%Y-%m-%dT%H:%M:%S.%f%z')
    day = calendar.day_name[date_time.weekday()]
    month = calendar.month_name[date_time.month][:3]
    date = f"{date_time.strftime('%d')} {month} {date_time.strftime('%m')}"
    time = f"{date_time.strftime('%H:%M')} GMT"
    event_json = {
        "day": day,
        "date": date,
        "time": time
    }
    return event_json


def format_short_name(short_name):
    return re.sub('(&)', r' \1 ', short_name)
