"""
Module for SQLInjectionStrategy Class.

This module provides the `SQLInjectionStrategy` class, a concrete implementation of the `ValidationStrategy` interface. The class is designed to validate input data by checking for patterns that may indicate SQL injection attempts, such as SQL keywords and suspicious operators.

Author: [Your Name]
Last Modified: [Date]
Status: In Testing, put logs

Dependencies:
    - re
    - validation_strategy_interface.ValidationStrategy

Classes:
    - SQLInjectionStrategy: Concrete validation strategy to detect potential SQL injection in input data.
"""
import re
from validation_strategy.validation_strategy_interface import ValidationStrategy

class SQLInjectionStrategy(ValidationStrategy):
    """
    SQLInjectionStrategy class.

    This class implements the `ValidationStrategy` interface and defines a validation strategy to check input data for
    potential SQL injection patterns. If any pattern indicative of SQL injection is detected, a warning message is returned.

    Attributes:
        - sql_patterns (list): A list of regular expressions used to identify potential SQL injection attempts.

    Methods:
        - validate(data): Checks if the data contains any SQL injection patterns and returns a warning if found.

    Example:
        sql_injection_validator = SQLInjectionStrategy()
        result = sql_injection_validator.validate({"input": "SELECT * FROM users"})
        if result:
            print(result)  # Output if SQL injection patterns are found
    """

    def __init__(self):
        """
        Initializes the SQLInjectionStrategy instance with SQL patterns.

        The `sql_patterns` attribute is a list of regular expressions that match common SQL injection patterns,
        such as SQL keywords (SELECT, INSERT, UPDATE, DELETE, etc.) and boolean-based SQL injection techniques
        (e.g., using OR/AND operators with conditional expressions).
        """
        self.sql_patterns = [
            r"(?i)\b(SELECT|INSERT|UPDATE|DELETE|DROP|ALTER|CREATE|EXEC)\b",
            r"(--|\bOR\b|\bAND\b)\s*\d+=\d+",
        ]
    
    def validate(self, data):
        """
        Validates the input data to check for potential SQL injection patterns.

        Args:
            data (dict): A dictionary where each value is a string to be checked for SQL injection patterns.

        Returns:
            str or None: A message indicating the presence of SQL injection patterns if any are found, otherwise None.

        Raises:
            ValueError: If `data` is not a dictionary or contains non-string values.

        Example:
            sql_injection_validator = SQLInjectionStrategy()
            result = sql_injection_validator.validate({"comment": "DROP TABLE users"})
            if result:
                print(result)  # Output if SQL injection patterns are found
        """
        for value in data.values():
            if isinstance(value, str):
                for pattern in self.sql_patterns:
                    if re.search(pattern, value):
                        return "Request contains potentially dangerous SQL keywords." 
        return None