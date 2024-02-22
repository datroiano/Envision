from datetime import datetime, timedelta
import time


def to_unix_time(datetime_str):
    try:
        dt_obj = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')
        return int(time.mktime(dt_obj.timetuple()) * 1000)
    except ValueError:
        return None  # Catch the error properly in use-case


def from_unix_time(unix_time_str):
    try:
        unix_time_ms = int(unix_time_str)
        dt_obj = datetime.fromtimestamp(unix_time_ms / 1000.0)
        formatted_datetime = dt_obj.strftime('%Y-%m-%d %H:%M:%S')
        return formatted_datetime
    except ValueError:
        return None


def previous_day(input_date):
    date_obj = datetime.strptime(input_date, '%Y-%m-%d')
    if date_obj.weekday() in [0, 6, 5]:  # Monday is 0, Sunday is 6, Saturday is 5
        previous_date = date_obj - timedelta(days=(date_obj.weekday() + 3) % 7)
    else:
        previous_date = date_obj - timedelta(days=1)
    return previous_date.strftime('%Y-%m-%d')
