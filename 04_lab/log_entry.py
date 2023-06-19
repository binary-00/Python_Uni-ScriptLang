# 6 (with 3. Enriching classes)
from dataclasses import dataclass
from datetime import datetime

@dataclass
class LogEntry:
    host: str
    timestamp: datetime
    request: str
    status_code: int
    size: int

    def __post_init__(self):
        self.timestamp = datetime.strptime(self.timestamp, "%d/%b/%Y:%H:%M:%S %z")

    def __str__(self): # How the str() func should behave
        return f'{self.host} - - [{self.timestamp.strftime("%d/%b/%Y:%H:%M:%S %z")}] "{self.request}" {self.status_code} {self.size}'

    def __repr__(self): #  # This __repr__ method returns a valid string py expression that can be used to recreate an equivalant object
        return f'LogEntry({self.host!r}, {self.timestamp.strftime("%d/%b/%Y:%H:%M:%S %z")!r}, {self.request!r}, {self.status_code!r}, {self.size!r})'

    def __eq__(self, other): # How '==' should behave when comparing instances of classes
        if isinstance(other, LogEntry):
            return (
                self.host == other.host
                and self.timestamp == other.timestamp
                and self.request == other.request
                and self.status_code == other.status_code
                and self.size == other.size
            )
        return False

    def __lt__(self, other): # How '<' should behave when comparing instances of classes
        if isinstance(other, LogEntry):
            return self.timestamp < other.timestamp
        return NotImplemented

    def __gt__(self, other): # How '>' should behave when comparing instances of classes
        if isinstance(other, LogEntry):
            return self.timestamp > other.timestamp
        return NotImplemented

    def __bool__(self): # bol() func. should behave when an instance of a class is called
        return bool(self.host and self.request)


# 3.2
def create_log_entry(line: str) -> LogEntry:
    host, timestamp, request, status_code, size = line.split()
    return LogEntry(host, timestamp, request[1:], int(status_code), int(size))

#3.3
def read_log_file(file_path: str) -> list[LogEntry]:
    with open(file_path) as f:
        return [LogEntry.create_log_entry(line.strip()) for line in f]
    
def display_requests_between(start_time: datetime, end_time: datetime, log_entries: list[LogEntry]) -> None:
    if end_time < start_time:
        print("Error: End time is earlier than start time.")
        return

    requests = [entry.request for entry in log_entries if start_time <= entry.timestamp <= end_time]
    requests.sort()
    for request in requests:
        print(request)

