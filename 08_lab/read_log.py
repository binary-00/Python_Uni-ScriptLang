import argparse
import re
from dataclasses import dataclass, field
from ipaddress import IPv4Network, IPv4Address
from typing import Dict, List


@dataclass
class Config:
    display: Dict[str, str] = field(default_factory=dict)
    log_file: str = ""
    config: Dict[str, str] = field(default_factory=dict)


@dataclass
class LogEntry:
    ip_address: str
    timestamp: str
    http_request_header: str
    http_status_code: str
    response_size: str


def read_config(filename: str) -> Config:
    section_header_pattern = re.compile(r"\[(.+)\]")
    section_content_pattern = re.compile(r"(.+)=(.+)")

    config = Config()

    try:
        with open(filename, "r") as f:
            for line in f:
                line = line.strip()
                section_header_match = section_header_pattern.match(line)
                if section_header_match:
                    section = section_header_match.group(1)
                else:
                    section_content_match = section_content_pattern.match(line)
                    if section_content_match:
                        key, value = section_content_match.groups()
                        if section == "Display":
                            config.display[key] = value
                        elif section == "LogFile":
                            config.log_file = value
                        elif section == "Config":
                            config.config[key] = value
    except FileNotFoundError:
        print(f'Error: Config file "{filename}" not found.')
        exit(1)

    # Set default values if not present in config file
    if "lines" not in config.display:
        config.display["lines"] = "10"
    if "separator" not in config.display:
        config.display["separator"] = ","
    if "filter" not in config.display:
        config.display["filter"] = "GET"

    return config


def read_log_file(filename: str) -> List[str]:
    try:
        with open(filename, "r") as f:
            return f.readlines()
    except FileNotFoundError:
        print(f'Error: Log file "{filename}" not found.')
        exit(1)


def analyze_log_file(log_lines: List[str]) -> List[LogEntry]:
    log_entry_pattern = re.compile(
        r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) - - \[(.+)\] "(.+)" (\d{3}) (\d+)'
    )
    log_entries = []

    for line in log_lines:
        match = log_entry_pattern.match(line)
        if match:
            (
                ip_address,
                timestamp,
                http_request_header,
                http_status_code,
                response_size,
            ) = match.groups()
            log_entry = LogEntry(
                ip_address,
                timestamp,
                http_request_header,
                http_status_code,
                response_size,
            )
            log_entries.append(log_entry)

    return log_entries


def parse_args():
    parser = argparse.ArgumentParser(
        description="Print all requests sent from the given IP subnet."
    )
    parser.add_argument(
        "--ip",
        type=str,
        required=True,
        help='The IP subnet to filter by (e.g. "192.168.0.0/24").',
    )
    parser.add_argument("--index", type=int, required=True, help="Your index number.")
    return parser.parse_args()


def ip_in_subnet(ip_address: str, subnet: IPv4Network) -> bool:
    return IPv4Address(ip_address) in subnet


def print_requests_from_subnet(
    log_entries: List[LogEntry], subnet: IPv4Network, lines_per_page: int
):
    count = 0
    for entry in log_entries:
        if ip_in_subnet(entry.ip_address, subnet):
            print(entry)
            count += 1
            if count == lines_per_page:
                input("Press Enter to continue...")
                count = 0


def count_bytes_sent(log_entries: List[LogEntry], filter: str, separator: str):
    total_bytes_sent = 0
    for entry in log_entries:
        if filter in entry.http_request_header:
            total_bytes_sent += int(entry.response_size)
    print(f"{filter}{separator}{total_bytes_sent}")


if __name__ == "__main__":
    args = parse_args()
    subnet = IPv4Network(args.ip)
    mask_length = args.index % 16 + 8
    subnet = subnet.supernet(new_prefix=mask_length)

    config = read_config("lab.config")

    lines_per_page = int(config.display["lines"])

    filter = config.display["filter"]
    separator = config.display["separator"]

    log_lines = read_log_file("access_log-20201025.txt")
    log_entries = analyze_log_file(log_lines)

    #print_requests_from_subnet(log_entries, subnet, lines_per_page)

    #count_bytes_sent(log_entries, filter, separator)
    #count_bytes_sent(log_entries, "POST", separator)
    #count_bytes_sent(log_entries, 'HEAD', separator)
    #count_bytes_sent(log_entries, 'DELETE', separator)
