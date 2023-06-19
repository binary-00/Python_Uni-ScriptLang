import unittest
from read_log import Config, LogEntry, read_config, read_log_file, analyze_log_file


class TestReadLog(unittest.TestCase):
    def test_read_config(self):
        config = read_config("lab.config")
        self.assertEqual(config.display["lines"], "10")
        self.assertEqual(config.display["separator"], ",")
        self.assertEqual(config.display["filter"], "GET")
        self.assertEqual(config.log_file, "access_log-20201025.txt")
        self.assertEqual(config.config["key"], "value")

    def test_read_log_file(self):
        log_lines = read_log_file("access_log-20201025.txt")
        self.assertEqual(len(log_lines), 3)
        self.assertEqual(
            log_lines[0],
            '127.0.0.1 - - [01/Jan/2022:00:00:00 +0000] "GET / HTTP/1.1" 200 1024\n',
        )
        self.assertEqual(
            log_lines[1],
            '127.0.0.2 - - [01/Jan/2022:00:01:00 +0000] "POST / HTTP/1.1" 201 2048\n',
        )
        self.assertEqual(
            log_lines[2],
            '127.0.0.3 - - [01/Jan/2022:00:02:00 +0000] "HEAD / HTTP/1.1" 200 512\n',
        )

    def test_analyze_log_file(self):
        log_lines = read_log_file("access_log-20201025.txt")
        log_entries = analyze_log_file(log_lines)
        self.assertEqual(len(log_entries), 3)
        self.assertEqual(log_entries[0].ip_address, "127.0.0.1")
        self.assertEqual(log_entries[0].timestamp, "01/Jan/2022:00:00:00 +0000")
        self.assertEqual(log_entries[0].http_request_header, "GET / HTTP/1.1")
        self.assertEqual(log_entries[0].http_status_code, "200")
        self.assertEqual(log_entries[0].response_size, "1024")


if __name__ == "__main__":
    unittest.main()
