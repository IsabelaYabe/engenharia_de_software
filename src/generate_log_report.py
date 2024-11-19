import os
import re
from datetime import datetime
from collections import defaultdict

class LogReportGenerator:
    def __init__(self, log_file):
        log_file_path = os.getenv('APP_LOG_PATH', os.path.dirname(__file__))
        self.log_file = os.path.join(log_file_path, log_file)
        self.log_entries = []
        self.operation_categories = {
            "table_operations": ["CREATE TABLE", "DELETE TABLE", "DROP TABLE"],
            "column_operations": ["ADD COLUMN", "DELETE COLUMN", "MODIFY COLUMN"],
            "row_operations": ["INSERT", "DELETE FROM", "UPDATE", "SEARCH"],
            "connection_operations": ["CONNECT", "INITIALIZE"],
            "test_results": ["TEST", "OK!!!"]
        }

    def read_log_file(self):
        if not os.path.exists(self.log_file):
            raise FileNotFoundError(f"Log file {self.log_file} does not exist")
        
        with open(self.log_file, "r") as file:
            self.log_entries = file.readlines()

    def generate_report(self):
        report = {
            "test_summary": defaultdict(int),
            "operations": defaultdict(list),
            "timing": defaultdict(float),
            "errors": []
        }

        current_test = None
        for entry in self.log_entries:
            timestamp, level, source, message = self.parse_log_entry(entry)
            
            # Process test results
            if "TEST" in message and "OK!!!" in message:
                test_num = re.search(r'TEST (\d+)', message)
                if test_num:
                    report["test_summary"]["total_tests"] += 1
                    report["test_summary"]["passed_tests"] += 1
                    current_test = int(test_num.group(1))

            # Categorize operations
            operation_type = self.categorize_operation(message)
            if operation_type:
                report["operations"][operation_type].append({
                    "timestamp": timestamp,
                    "source": source,
                    "message": message.strip(),
                    "test_context": current_test
                })

            # Track errors
            if level == "ERROR":
                report["errors"].append({
                    "timestamp": timestamp,
                    "source": source,
                    "message": message.strip()
                })

        return report

    def parse_log_entry(self, entry):
        parts = entry.split(" | ")
        timestamp = parts[0]
        level = parts[1]
        source = parts[2].split(":")[0]
        message = parts[3]
        return timestamp, level, source, message

    def categorize_operation(self, message):
        for category, keywords in self.operation_categories.items():
            if any(keyword in message.upper() for keyword in keywords):
                return category
        return "other"

    def generate_html_report(self, report):
        html = """
        <html>
        <head>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; }
                .section { margin-bottom: 20px; }
                .error { color: red; }
                .success { color: green; }
            </style>
        </head>
        <body>
        """

        # Test Summary
        html += "<h2>Test Summary</h2>"
        total = report["test_summary"]["total_tests"]
        passed = report["test_summary"]["passed_tests"]
        html += f"<p>Total Tests: {total}<br>"
        html += f"Passed Tests: {passed}<br>"
        html += f"Success Rate: {(passed/total*100 if total else 0):.2f}%</p>"

        # Operations Summary
        for category, operations in report["operations"].items():
            html += f"<h3>{category.replace('_', ' ').title()}</h3>"
            for op in operations:
                html += f"<p>{op['timestamp']} - {op['message']}</p>"

        # Errors
        if report["errors"]:
            html += "<h3>Errors</h3>"
            for error in report["errors"]:
                html += f"<p class='error'>{error['timestamp']} - {error['message']}</p>"

        html += "</body></html>"
        return html

    def save_report(self, report, output_format="html"):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        if output_format == "html":
            html_content = self.generate_html_report(report)
            output_file = f"database_report_{timestamp}.html"
            with open(output_file, "w") as f:
                f.write(html_content)
            return output_file

if __name__ == "__main__":
    generator = LogReportGenerator("app.log")
    generator.read_log_file()
    report = generator.generate_report()
    output_file = generator.save_report(report)
    print(f"Report generated: {output_file}")