"""
Module for BannedWordsStrategy Class.

This module defines the `BannedWordsStrategy` class, which is a concrete implementation of the `ValidationStrategy` interface. The class is responsible for validating input data against a predefined set of banned words, returning a warning if banned words are found.

Author: Isabela Yabe 
Last Modified: 20/11/2024
Status: Complete

Dependencies:
    - json
    - os
    - sys
    - validation_strategy_interface.ValidationStrategy
    - custom_logger.setup_logger

Classes:
    - BannedWordsStrategy: Concrete validation strategy that checks for banned words in data.
"""

import json
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "src")))
from validation_endpoints_strategy.validation_strategy_interface import ValidationStrategy 
from custom_logger import setup_logger

logger = setup_logger()

class BannedWordsStrategy(ValidationStrategy):
    """
    BannedWordsStrategy class.

    This class implements the `ValidationStrategy` interface and defines a specific validation strategy that checks
    input data for banned words. If banned words are found, a message with the offending words is logged and returned.

    Attributes:
        - banned_words (set): A set of banned words loaded from a JSON file.

    Methods:
        - validate(data): Checks if the data contains any banned words and returns a warning message if so.

    Example:
        banned_words_validator = BannedWordsStrategy()
        result = banned_words_validator.validate({"text": "This is some input text"})
        if result:
            print(result)  # Output if banned words are found
    """
    def __init__(self):
        """
        Initializes the BannedWordsStrategy instance by loading the banned words from a JSON file.
        
        The banned words are stored in a JSON file located at "../data/json/banned_words.json".
        """
        json_path = os.path.join(os.path.dirname(__file__), "..", "..", "data", "json", "banned_words.json")
        try:
            with open(json_path, "r", encoding="utf-8") as file:
                self.banned_words = set(json.load(file)["banned_words"])
            logger.info("Banned words loaded successfully.")
        except FileNotFoundError:
            logger.error(f"Banned words file not found at {json_path}.")
            raise
        except json.JSONDecodeError:
            logger.error(f"Error decoding JSON from file at {json_path}.")
            raise

    def validate(self, data):
        """
        Validates the input data to check for banned words.

        Args:
            data (dict): A dictionary of data where each value is a string to be checked for banned words.

        Returns:
            str or None: A message indicating the presence of banned words if any are found, otherwise None.

        Raises:
            ValueError: If `data` is not a dictionary or if any non-string values are encountered.

        Example:
            banned_words_validator = BannedWordsStrategy()
            result = banned_words_validator.validate({"comment": "Example comment"})
            if result:
                print(result)  # Output if banned words are found
        """
        if not isinstance(data, dict):
            logger.error("Input data must be a dictionary")
            raise ValueError("Input data must be a dictionary")

        banned_words_found = []

        for value in data.values():
            if isinstance(value, str):
                words = value.lower().split()
                for word in words:
                    if word in self.banned_words:
                        banned_words_found.append(word)
            else:
                logger.error("All values in input data must be strings")
                raise ValueError("All values in input data must be strings")

        if banned_words_found:
            message = f"Request contains banned words: {", ".join(banned_words_found)}"
            logger.warning(message)
            return message

        logger.info("Request does not contain banned words.")
        return None