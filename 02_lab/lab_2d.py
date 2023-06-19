import sys

def image_download_ratio():
    image_count = 0
    other_count = 0

    for line in sys.stdin:
        try:
            # from NASA, 6th string position ends with resource type
            path = line.split()[6]

            if path.endswith(('.gif', '.jpg', '.jpeg', '.xbm')):
                image_count += 1
            else:
                other_count += 1
        except IndexError:
            continue
    if other_count == 0:
        print("Non-image resouruce")
    else:
        ratio = image_count / other_count
        print(f"Image download ratio: {ratio:.2f}")
if __name__ == '__main__':
    image_download_ratio()