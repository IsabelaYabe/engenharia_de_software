"""
Module for testing the immutable_fields decorator.

This module contains unit tests for verifying the functionality of the `immutable_fields` decorator,
which ensures that specified fields in a database cannot be updated. The tests use the `MockDatabase` 
class to simulate a database with immutable fields and validate the behavior of the decorator.

Author: Isabela Yabe
Last Modified: 20/11/2024
Status: Complete

Dependencies:
    - unittest
    - unittest.mock.MagicMock
    - unittest.mock.patch
    - custom_logger.setup_logger
    - decorators_method.immutable_fields
    - utils.utils.tuple_to_dict
"""

import unittest
from unittest.mock import MagicMock, patch

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.getcwd(),"src")))
from custom_logger import setup_logger
from decorators_method import immutable_fields
from utils.utils import tuple_to_dict

logger = setup_logger()

class TestImmutableFieldsDecorator(unittest.TestCase):
    """
    Unit tests for the `immutable_fields` decorator.

    This class validates the behavior of the `immutable_fields` decorator by using a mock database 
    to simulate record updates while respecting immutability constraints.
    """
    def setUp(self):
        """
        Setup a mock class and methods to test the immutable_fields decorator.
        """
        class MockDatabase:
            def __init__(self):
                self.immutable_columns = ["col2"]
                self.columns = ["id", "col1", "col2", "col3", "col_id"]

            def get_by_id(self, record_id):
                """
                Mock method to simulate fetching a record by ID.
                """
                if record_id == "1":
                    return ("1", "value_1", "value_2", "value_3", "value_id")  
                return None
            
            @immutable_fields("immutable_columns")
            def update_record(self, record_id, **kwargs):
                """
                Mock method to simulate updating a record.
                """
                logger.info(f"Record {record_id} updated with {kwargs}")
                return kwargs
        
        self.MockDatabase = MockDatabase()

    @patch("utils.utils.tuple_to_dict")
    def test_update_allowed_fields(self, mock_tuple_to_dict):
        """
        Test updating fields that are not immutable.
        """
        mock_tuple_to_dict.return_value = {
            "id": "1",
            "col1": "value_1",
            "col2": "value_2",
            "col3": "value_3",
            "col_id": "value_id"
        }
        result = self.MockDatabase.update_record("1", col1="new_value_1")
        self.assertEqual(result, {"col1": "new_value_1"})
        logger.info("Test update allowed fields: OK!!! ---------------------------> TEST 1 OK!!!")

    @patch("utils.utils.tuple_to_dict")
    def test_update_immutable_field(self, mock_tuple_to_dict):
        """
        Test updating an immutable field raises ValueError.
        """
        mock_tuple_to_dict.return_value = {
            "id": "1",
            "col1": "value_1",
            "col2": "value_2",
            "col3": "value_3",
            "col_id": "value_id"
        }
        with self.assertRaises(ValueError) as context:
            self.MockDatabase.update_record("1", col_id="new_value_id")

        self.assertEqual(
            str(context.exception),
            "The col_id field is immutable and cannot be updated"
        )
        logger.info("Test update immutable field: OK!!! ---------------------------> TEST 2 OK!!!")
    
    @patch("utils.utils.tuple_to_dict")
    def test_update_immutable_field_id(self, mock_tuple_to_dict):
        """
        Test updating an immutable field raises ValueError.
        """
        mock_tuple_to_dict.return_value = {
            "id": "1",
            "col1": "value_1",
            "col2": "value_2",
            "col3": "value_3",
            "col_id": "value_id"
        }
        with self.assertRaises(ValueError) as context:
            self.MockDatabase.update_record("1", id="2")

        self.assertEqual(
            str(context.exception),
            "The id field is immutable and cannot be updated"
        )
        logger.info("Test update immutable id field: OK!!! ---------------------------> TEST 3 OK!!!")

    @patch("utils.utils.tuple_to_dict")
    def test_record_not_found(self, mock_tuple_to_dict):
        """
        Test attempting to update a non-existent record raises ValueError.
        """
        mock_tuple_to_dict.return_value = None
        with self.assertRaises(ValueError) as context:
            self.MockDatabase.update_record("999", col1="Nonexistent")

        self.assertEqual(
            str(context.exception),
            "Record with ID 999 not found"
        )
        logger.info("Test record not found: OK!!! ---------------------------> TEST 4 OK!!!")

if __name__ == "__main__":
    unittest.main()
