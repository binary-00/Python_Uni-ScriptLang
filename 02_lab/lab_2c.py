import sys

def largest_resource():
    max_path = 0
    max_size = 0

    for line in sys.stdin:
        try:
            # from NASA, path is in 6th position & size in the last
            parts = line.split()
            path = parts[6]
            size = int(parts[-1])

            if size > max_size:
                max_size = size
                max_path = path
        except (IndexError, ValueError): # valid range and valid input
            continue

    print(f"Path and Size of largest resource: {max_path} {max_size}bytes")
if __name__ == '__main__':
    largest_resource()