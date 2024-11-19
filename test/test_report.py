import unittest
import os
import re
from datetime import datetime
from collections import defaultdict

class TestLogReport(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.log_file_path = os.getenv('APP_LOG_PATH', os.path.dirname(__file__))
        cls.log_file = os.path.join(cls.log_file_path, "app.log")
        cls.test_patterns = {
            "timestamp": r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}$",
            "log_entry": r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3} \| (INFO|ERROR|WARNING) \| [\w:]+ - .+$",
            "test_result": r"TEST \d+ OK!!!"
        }
        cls.expected_logs = [
            "Test connect: OK!!! ---------------------------> TEST 1 OK!!!",
            "Test modify column sucess: OK!!! ---------------------------> TEST 2 OK!!!",
            "Test modify column column id error: OK!!! ---------------------------> TEST 3 OK!!!",
            "Test add column column not null true: OK!!! ---------------------------> TEST 4 OK!!!",
            "Test add column column not null false: OK!!! ---------------------------> TEST 5 OK!!!",
            "Test delete column: OK!!! ---------------------------> TEST 6 OK!!!",
            "Test delete rows: OK!!! ---------------------------> TEST 7 OK!!!",
            "Test delete rows not found: OK!!! ---------------------------> TEST 8 OK!!!",
            "Test regex to get table name: OK!!! ---------------------------> TEST 9 OK!!!",
            "Test create non exist table: OK!!! ---------------------------> TEST 10 OK!!!",
            "Test create exist table: OK!!! ---------------------------> TEST 11 OK!!!",
            "Test delete table: OK!!! ---------------------------> TEST 12 OK!!!",
            "Test insert row: OK!!! ---------------------------> TEST 13 OK!!!",
            "Test update row: OK!!! ---------------------------> TEST 14 OK!!!",
            "Test get by id: OK!!! ---------------------------> TEST 15 OK!!!",
            "Test get by id not: OK!!! ---------------------------> TEST 16 OK!!!",
            "Test search record: OK!!! ---------------------------> TEST 17 OK!!!",
            "Test execute sql: OK!!! ---------------------------> TEST 18 OK!!!"
        ]

    def setUp(self):
        self.assertTrue(os.path.exists(self.log_file), f"Log file not found at {self.log_file}")
        with open(self.log_file, "r") as file:
            self.log_content = file.read()
            self.log_entries = file.readlines()
        self.test_statistics = self.calculate_test_statistics()

    def calculate_test_statistics(self):
        stats = defaultdict(int)
        for entry in self.log_entries:
            if "TEST" in entry and "OK!!!" in entry:
                stats["total_tests"] += 1
                if "ERROR" not in entry:
                    stats["passed_tests"] += 1
        return stats

    def test_log_file_basics(self):
        """Test basic log file properties"""
        self.assertTrue(os.path.getsize(self.log_file) > 0, "Log file is empty")
        self.assertTrue(self.log_content.strip(), "Log content is empty")

    def test_expected_test_results(self):
        """Test presence of expected test results"""
        for expected_log in self.expected_logs:
            self.assertIn(
                expected_log, 
                self.log_content, 
                f"Missing test result: {expected_log}"
            )

    def test_log_entry_structure(self):
        """Test structure of log entries"""
        pattern = re.compile(self.test_patterns["log_entry"])
        for i, entry in enumerate(self.log_entries, 1):
            self.assertRegex(
                entry, 
                pattern, 
                f"Invalid log entry structure at line {i}: {entry}"
            )

    def test_log_entry_components(self):
        """Test individual components of log entries"""
        for i, entry in enumerate(self.log_entries, 1):
            parts = entry.split(" | ")
            self.assertEqual(len(parts), 4, f"Invalid parts count at line {i}")
            timestamp, level, source, message = parts
            
            self.assertRegex(
                timestamp,
                self.test_patterns["timestamp"],
                f"Invalid timestamp at line {i}"
            )
            self.assertIn(
                level,
                ["INFO", "ERROR", "WARNING"],
                f"Invalid log level at line {i}"
            )
            self.assertTrue(
                source.strip().endswith(":"),
                f"Invalid source format at line {i}"
            )
            self.assertTrue(
                message.strip(),
                f"Empty message at line {i}"
            )

    def test_chronological_order(self):
        """Test that log entries are in chronological order"""
        timestamps = []
        for entry in self.log_entries:
            timestamp = entry.split(" | ")[0]
            timestamps.append(datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S,%f"))
        
        self.assertEqual(
            timestamps,
            sorted(timestamps),
            "Log entries are not in chronological order"
        )

    def test_test_statistics(self):
        """Test statistics of test results"""
        self.assertEqual(
            self.test_statistics["total_tests"],
            18,
            "Unexpected total number of tests"
        )
        self.assertEqual(
            self.test_statistics["passed_tests"],
            self.test_statistics["total_tests"],
            "Not all tests passed"
        )

    def test_error_handling(self):
        """Test error logging"""
        error_entries = [
            entry for entry in self.log_entries 
            if "ERROR" in entry.split(" | ")[1]
        ]
        for error in error_entries:
            self.assertIn(
                "ERROR",
                error,
                "Error entry not properly formatted"
            )

    def tearDown(self):
        self.log_content = None
        self.log_entries = None
        self.test_statistics = None

if __name__ == "__main__":
    unittest.main(verbosity=2)