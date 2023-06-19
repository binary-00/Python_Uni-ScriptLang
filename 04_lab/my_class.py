# 1
from datetime import datetime
# 7.1
from log_entry import LogEntry

def log_timestamp_to_datetime(timestamp: str):
    return datetime.strptime(timestamp, "%d/%b/%Y:%H:%M:%S %z")


timestamp = "18/Oct/2020:01:30:42 +0200"
dt = log_timestamp_to_datetime(timestamp)
#print(dt)


# 2
class HttpRequest:
    def __init__(
        self, host: str, timestamp: str, request: str, status_code: int, size: int
    ):
        self.host = host
        self.timestamp = datetime.strptime(timestamp, "%d/%b/%Y:%H:%M:%S %z")
        self.request = request
        self.status_code = status_code
        self.size = size

    def __str__(self):
        return f'{self.host} - [{self.timestamp.strftime("%d/%b/%Y:%H:%M:%S %z")}] "{self.request}" {self.status_code} {self.size}'

    def get_request_method(self):
        return self.request.split(" ")[0]

    def get_requested_resource(self):
        return self.request.split(" ")[1]
    

# 3
class LogEntry:
    def __init__(
        self, host: str, timestamp: str, request: str, status_code: int, size: int
    ):
        self.host = host
        self.timestamp = datetime.strptime(timestamp, "%d/%b/%Y:%H:%M:%S %z")
        self.request = request
        self.status_code = status_code
        self.size = size

    def __str__(self):
        return f'{self.host} - - [{self.timestamp.strftime("%d/%b/%Y:%H:%M:%S %z")}] "{self.request}" {self.status_code} {self.size}'


# 4
class MalformedHttpRequest(LogEntry):
    def __init__(self, host: str, timestamp: str, request: str):

        super().__init__(host, timestamp, request, None, None)

    def __str__(self):

        return f'{self.host} - - [{self.timestamp.strftime("%d/%b/%Y:%H:%M:%S %z")}] "{self.request}" - -'


class CorrectHttpRequest(LogEntry):
    def __init__(
        self, host: str, timestamp: str, request: str, status_code: int, size: int
    ):

        super().__init__(host, timestamp, request, status_code, size)

    # 5.1
    @property
    def is_successful(self):

        return 200 <= self.status_code < 300

    # 5.2
    @property
    def is_error(self):

        return 400 <= self.status_code < 600


# 7.2
log_entry = LogEntry(
    "199.72.81.55",
    "01/Jul/1995:00:00:01 -0400",
    "GET /history/apollo/ HTTP/1.0",
    200,
    6245,
)

print(log_entry)

