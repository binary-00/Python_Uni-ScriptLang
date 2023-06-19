import sys
from datetime import datetime

def filter_frydays(): #weekday()
    for line in sys.stdin:
        try:
            timestamp_str = line.split()[3].strip('[]')
            timestamp = datetime.strptime(timestamp_str, "%d/%b/%Y:%H:%M:%S")

            if timestamp.weekday() == 4: 
                print(line, end='')
        except (IndexError, ValueError):
            continue

if __name__ == '__main__':
    filter_frydays()