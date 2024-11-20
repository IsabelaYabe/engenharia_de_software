"""
Module for SQLInjectionStrategy Class.

This module provides the `SQLInjectionStrategy` class, a concrete implementation of the `ValidationStrategy` interface. The class is designed to validate input data by checking for patterns that may indicate SQL injection attempts, such as SQL keywords and suspicious operators.

Author: Isabela Yabe
Last Modified: 20/11/2024
Status: Complete

Dependencies:
    - re
    - validation_strategy_interface.ValidationStrategy
    - custom_logger.setup_logger

Classes:
    - SQLInjectionStrategy: Concrete validation strategy to detect potential SQL injection in input data.
"""

import re
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "src")))
from validation_endpoints_strategy.validation_strategy_interface import ValidationStrategy
from custom_logger import setup_logger

logger = setup_logger()

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
            r"(?i)\b(SELECT|INSERT|UPDATE|DELETE|DROP|ALTER|CREATE|EXEC)\b",  # Matches SQL commands
            r"(--|\bOR\b|\bAND\b)\s*\d+=\d+",  # Matches comments or boolean-based injections
        ]
        logger.info("SQL injection patterns initialized.")

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
        if not isinstance(data, dict):
            logger.error("Input data must be a dictionary")
            raise ValueError("Input data must be a dictionary")

        for key, value in data.items():
            if not isinstance(value, str):
                logger.error(f"Non-string value found for key {key}. All values must be strings")
                raise ValueError(f"Value for key {key} must be a string")

            for pattern in self.sql_patterns:
                if re.search(pattern, value):
                    message = f"Request contains potentially dangerous SQL keywords in {key}"
                    logger.warning(message)
                    return message

        logger.info("Request does not contain SQL injection patterns")
        return None
