import sys

def total_data_sent():
    total_bytes = 0

    for line in sys.stdin:
        try:
            # number of bytes sent is in the last column
            bytes_sent = int(line.split()[-1])
            total_bytes += bytes_sent
        except ValueError:
            # continues if there was no data sent
            continue
    
    total_gigabytes = total_bytes / (1024 ** 3)
    print(f"Total data sent to host : {total_gigabytes:.2f} GB") # round up to 2 decimal places (.2f)

if __name__ == '__main__':
    total_data_sent()