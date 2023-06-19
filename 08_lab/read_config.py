import re
from dataclasses import dataclass, field
from typing import Dict


@dataclass
class Config:
    display: Dict[str, str] = field(default_factory=dict)
    log_file: str = ""
    config: Dict[str, str] = field(default_factory=dict)


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


config = read_config("lab.config")
print(config.display)
print(config.log_file)
print(config.config)
