
def to_unix_time(datetime_str):
    try:
        from datetime import datetime
        import time
        dt_obj = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')
        return str(int(time.mktime(dt_obj.timetuple()) * 1000))
    except ValueError:
        return None  # Catch the error properly in use-case

