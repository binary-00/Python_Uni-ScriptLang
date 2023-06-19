import sys
from datetime import datetime

def filter_time_range():
    start_time = datetime.strptime("22:00", "%H:%M").time() # parse datetime, creates time obj
    end_time = datetime.strptime("06:00", "%H:%M").time()

    for line in sys.stdin:
        try:
            # time stamp in 3rd position
            timestamp_str = line.split()[3].strip('[]')
            timestamp = datetime.strptime(timestamp_str, "%d/%b/%Y:%H:%M:%S")
            time = timestamp.time()

            if (start_time <= end_time and start_time <= time <= end_time) or \
               (start_time > end_time and (time >= start_time or time <= end_time)):
                print(line, end='')
        except (IndexError, ValueError):
            continue

if __name__ == '__main__':
    filter_time_range()