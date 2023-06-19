import sys

def filter_response_code():
    for line in sys.stdin:
        try:
            # in the 8th position
            response_code = int(line.split()[8])

            if response_code == 404:
                print(line, end='')
        except (IndexError, ValueError):
            continue
if __name__ == '__main__':
    filter_response_code()