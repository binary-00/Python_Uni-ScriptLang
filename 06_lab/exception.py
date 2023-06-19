import json
import logging

config = {}

config['webserver_log'] = input('Enter the name of the webserver log: ')
config['http_request_method'] = input('Enter the name of one of the HTTP request methods to be used as a filter for displaying: ')
config['logging_level'] = input('Enter the logging level used by the application: ')
config['log_lines_displayed'] = int(input('Enter the number of log lines to be displayed at once: '))
config['custom_parameter'] = input('Enter your own parameter: ')

with open('config.json', 'w', encoding='utf-8') as f:
    json.dump(config, f, ensure_ascii=False, indent=4)

class ConfigError(Exception):
    pass

def read_config():
    try:
        with open('config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
    except FileNotFoundError:
        raise ConfigError('Configuration file does not exist')
    except json.JSONDecodeError:
        raise ConfigError('Configuration file is not a correct JSON file')

    required_keys = ['webserver_log', 'http_request_method', 'logging_level', 'log_lines_displayed', 'custom_parameter']
    for key in required_keys:
        if key not in config:
            raise ConfigError(f'Configuration file does not contain required value: {key}')

    return config

def setup_logging(config):
    log_levels = {
        'DEBUG': logging.DEBUG,
        'INFO': logging.INFO,
        'WARNING': logging.WARNING,
        'ERROR': logging.ERROR,
        'CRITICAL': logging.CRITICAL
    }

    log_level = config.get('logging_level')
    if log_level not in log_levels:
        raise ConfigError(f'Invalid logging level: {log_level}')

    logging.basicConfig(level=log_levels[log_level])

def print_config():
    try:
        with open('config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
        for key, value in config.items():
            print(f"{key}: {value}")
    except FileNotFoundError:
        raise ConfigError('Configuration file does not exist')
    except json.JSONDecodeError:
        raise ConfigError('Configuration file is not a correct JSON file')


def main():
    try:
        config = read_config()
        setup_logging(config)
    except ConfigError as e:
        print(f'Error: {e}')
    finally:
        print('Program finished')

if __name__ == '__main__':
    main()
    print_config()