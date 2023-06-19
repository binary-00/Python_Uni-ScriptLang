"""Main module."""
import sys
import logging

def read_log():
    try:
        lines = sys.stdin.readlines()
        logging.debug(f'Number of lines read: {len(lines)}')
        entries = [tuple(line.split()) for line in lines if line.strip()]
        entries = [(str(entry[0]).strip(), str(entry[1]).strip(), str(entry[2]).strip(), str(entry[3]).strip(),
                    str(entry[4]).strip(), str(entry[5]).strip(), int(entry[6]) if entry[6].isdigit() else entry[6],
                    int(entry[7]) if entry[7].isdigit() else entry[7]) for entry in entries]
    except Exception as e:
        logging.error(f'An error occurred while reading the log: {e}')
    else:
        logging.debug(f'Number of entries in the list: {len(entries)}')
    return entries

def get_successful_reads(entries):
    successful_reads = [entry for entry in entries if isinstance(entry[7], int) and 200 <= entry[7] < 300]
    logging.info(f'Number of entries in the resulting list: {len(successful_reads)}')
    return successful_reads


def get_failed_reads(entries, separate_lists=False):
    http_4xx = [entry for entry in entries if isinstance(entry[7], int) and 400 <= entry[7] < 500]
    http_5xx = [entry for entry in entries if isinstance(entry[7], int) and 500 <= entry[7] < 600]
    logging.info(f'Number of entries with 4xx result codes: {len(http_4xx)}')
    logging.info(f'Number of entries with 5xx result codes: {len(http_5xx)}')
    if separate_lists:
        return http_4xx, http_5xx
    else:
        return http_4xx + http_5xx

def get_entries_by_code(entries, status_code):
    if not isinstance(status_code, int) or status_code < 100 or status_code >= 600:
        raise ValueError('Invalid status code')
    entries_with_code = [entry for entry in entries if isinstance(entry[7], int) and entry[7] == status_code]
    logging.info(f'Number of entries with status code {status_code}: {len(entries_with_code)}')
    return entries_with_code

def get_entries_by_extension(entries, extension):
    entries_with_extension = [entry for entry in entries if isinstance(entry[6], str) and entry[6].endswith(extension)]
    logging.info(f'Number of entries with extension "{extension}": {len(entries_with_extension)}')
    return entries_with_extension

'''def print_entries(entries):
    for entry in entries:
        print(entry)
    entries = []
    print_entries(entries)'''

def run():
    entries = read_log()

    # Get successful reads and print them
    #successful_reads = get_successful_reads(entries)
    #print(successful_reads)

    # Get failed reads and print them
    #http_4xx, http_5xx = get_failed_reads(entries, separate_lists=True)
    #print(http_4xx)
    #print(http_5xx)
    
    # Get entries with status code (ex:200)
    #entries_with_code = get_entries_by_code(entries, 302)
    #print(entries_with_code)

    # Get entries with extensions
    entries_with_extension = get_entries_by_extension(entries, "html")
    #print(entries_with_extension)

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    run()