import sys

def filter_poland():
    for line in sys.stdin:
        try:
            host = line.split()[0]

            if host.endswith('.pl'):
                print(line, end='')
        except IndexError:
            continue

if __name__ == '__main__':
    filter_poland()