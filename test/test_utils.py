"""
Module to test the utility functions in the `utils` module.

Author: Isabela Yabe
Last Modified: 20/11/2024
Status: Complete

Dependencies:
    - unittest
    - utils.utils.tuple_rows_to_dict
    - utils.utils.tuple_to_dict
    - custom_logger.setup_logger
"""
import unittest

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "src")))
from utils.utils import tuple_rows_to_dict, tuple_to_dict
from custom_logger import setup_logger

logger = setup_logger()

class TestTupleToDictFunctions(unittest.TestCase):
    def setUp(self):
        """
        Set up sample data for testing the tuple to dictionary conversion functions.
        """
        self.sample_tuples = [
            (1, "Alice", 25, "Engineer"),
            (2, "Bob", 30, "Designer"),
            (3, "Charlie", 35, "Manager")
        ]
        self.columns = ["id", "name", "age", "occupation"]

        self.single_tuple = (4, "Diana", 40, "Architect")

    def test_tuple_rows_to_dict(self):
        """
        Test the `tuple_rows_to_dict` function to ensure it correctly converts
        a list of tuples into a list of dictionaries.
        """
        expected_output = [
            {"id": 1, "name": "Alice", "age": 25, "occupation": "Engineer"},
            {"id": 2, "name": "Bob", "age": 30, "occupation": "Designer"},
            {"id": 3, "name": "Charlie", "age": 35, "occupation": "Manager"}
        ]
        result = tuple_rows_to_dict(self.sample_tuples, self.columns)
        self.assertEqual(result, expected_output)
        logger.info("Test tuple rows to dict: OK!!! ---------------------------> TEST 1 OK!!!")
        

    def test_tuple_to_dict(self):
        """
        Test the `tuple_to_dict` function to ensure it correctly converts
        a single tuple into a dictionary.
        """
        expected_output = {"id": 4, "name": "Diana", "age": 40, "occupation": "Architect"}
        result = tuple_to_dict(self.single_tuple, self.columns)
        self.assertEqual(result, expected_output)
        logger.info("Test tuple to dict: OK!!! ---------------------------> TEST 2 OK!!!")

    def test_empty_list_input(self):
        """
        Test the `tuple_rows_to_dict` function with an empty list to ensure it returns an empty list.
        """
        result = tuple_rows_to_dict([], self.columns)
        self.assertEqual(result, [])
        logger.info("Test tuple rows to dict with empty list: OK!!! ---------------------------> TEST 3 OK!!!")

    def test_empty_tuple_input(self):
        """
        Test the `tuple_to_dict` function with an empty tuple to ensure it returns an empty dictionary.
        """
        result = tuple_to_dict((), [])
        self.assertEqual(result, {})
        logger.info("Test tuple to dict with empty tuple: OK!!! ---------------------------> TEST 4 OK!!!")

    def test_mismatched_columns_length(self):
        """
        Test the `tuple_to_dict` function to ensure it raises an error if the length
        of the columns and tuple do not match.
        """
        with self.assertRaises(IndexError):
            tuple_to_dict((1, "Alice"), ["id", "name", "age"])
        logger.info("Test mismatched columns length: OK!!! ---------------------------> TEST 5 OK!!!")

if __name__ == "__main__":
    unittest.main()
