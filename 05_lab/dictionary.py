import sys

# 1
class LogEntry:
    def __init__(self, ip, timestamp, request, status_code, size):
        self.ip = ip
        self.timestamp = timestamp
        self.request = request
        self.status_code = status_code
        self.size = size


def read_log():
    log_dict = {}
    for line in sys.stdin:
        parts = line.split()
        if len(parts) < 10:
            continue
        ip = parts[0]
        timestamp = parts[3] + " " + parts[4]
        request = " ".join(parts[5:8])
        status_code = parts[8]
        size = parts[9]
        log_entry = LogEntry(ip, timestamp, request, status_code, size)
        if ip not in log_dict:
            log_dict[ip] = []
        log_dict[ip].append(log_entry)
    return log_dict


# 2
class RequestCounter:
    def __init__(self):
        self.requests = {}

    def add_request(self, ip):
        if ip not in self.requests:
            self.requests[ip] = 0
        self.requests[ip] += 1


def ip_requests(log_dict):
    counter = RequestCounter()
    for key, value in log_dict.items():
        for entry in value:
            counter.add_request(entry.ip)
    return counter


# 3
def ip_find(counter, most_active=True):
    if not counter.requests:
        return []
    if most_active:
        max_requests = max(counter.requests.values())
        return [ip for ip, count in counter.requests.items() if count == max_requests]
    else:
        min_requests = min(counter.requests.values())
        return [ip for ip, count in counter.requests.items() if count == min_requests]


# 4
def longest_request(log_dict):
    max_length = 0
    longest_entry = None
    for key, value in log_dict.items():
        for entry in value:
            if len(entry.request) > max_length:
                max_length = len(entry.request)
                longest_entry = entry
    return longest_entry.ip, longest_entry.request


# 5
def non_existent(log_dict):
    requests = set()
    for key, value in log_dict.items():
        for entry in value:
            if entry.status_code == "404":
                requests.add(entry.request)
    return list(requests)


if __name__ == "__main__":
    log_dict = read_log()

    counter = ip_requests(log_dict)
    most_active_ips = ip_find(counter, most_active=True)
    least_active_ips = ip_find(counter, most_active=False)
    #print(f"Most active IPs: {most_active_ips}")
    #print(f"Least active IPs: {least_active_ips}")

    ip, request = longest_request(log_dict)
    #print(f"Longest request: {request} (from IP {ip})")

    requests = non_existent(log_dict)
    #print(f"Requests with 404 status code: {requests}")