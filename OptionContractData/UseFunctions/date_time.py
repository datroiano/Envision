from datetime import datetime
import time


def to_unix_time(datetime_str):
    try:
        dt_obj = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')
        return str(int(time.mktime(dt_obj.timetuple()) * 1000))
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
