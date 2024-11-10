"""
Module for Testing Immutable Fields Decorator in Database Manager.

This module contains unit tests for the `immutable_fields` decorator used in the `DatabaseManagerConcrete` class. 
The `immutable_fields` decorator ensures that certain fields in the database are immutable and cannot be updated. 
This module validates that only mutable fields can be modified in the `update_row` method and raises errors when immutable fields are modified.

Author: Isabela Yabe
Last Modified: 09/11/2024
Status: Complete

Dependencies:
    - unittest
    - unittest.mock (patch, MagicMock)
    - flask
    - sys
    - os
    - database_manager.DatabaseManager
    - decorators.immutable_fields

Classes:
    - TestDatabaseManagerConcrete: A concrete class inheriting from DatabaseManager to test update functionality.
    - TestImmutableFields: Unit tests for checking the `immutable_fields` decorator behavior.
"""
import unittest
from unittest.mock import MagicMock, patch
from flask import Flask, jsonify, request

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), 'src')))
from database_manager import DatabaseManager
from decorators import immutable_fields

class TestDatabaseManagerConcrete(DatabaseManager):
    """
    A concrete subclass of DatabaseManager to enable testing of update operations with immutable fields.

    Methods:
        - update_row(record_id, **kwargs): Uses the `immutable_fields` decorator to enforce immutability on certain fields.
        - get_by_id(record_id): Mocked to simulate fetching a record by ID.
        - insert_row(value1, value2, value3): Mock method to simulate insertion of a row.
    """
    def __init__(self,host, user, password, database):
        super().__init__(host, user, password, database, "test_table")
        self.columns = ["id", "col1", "col2", "col3"]
        self._create_table()

    def _create_table(self): ...
    
    @immutable_fields(["id", "col1", "col2"])
    def update_row(self, record_id, **kwargs):
        return self._update_row(record_id, "id", **kwargs)
    
    def get_by_id(self, record_id):
        return {
            "id": record_id,
            "col1": "old_value1",
            "col2": "old_value2",
            "col3": 100.00
        }

    def insert_row(self, value1, value2, value3): 
        row_id = "123e4567-e89b-12d3-a456-426614174000"
        return row_id
    
    def delete_row(self, record_id): ...

class TestImmutableFields(unittest.TestCase):
    """
    Unit test case for validating the behavior of the `immutable_fields` decorator.

    Methods:
        - setUp: Sets up a mock database connection and initializes a mock database manager instance.
        - test_update_non_immutable_field: Tests that updating a non-immutable field works without errors.
        - test_update_immutable_field: Tests that attempting to update an immutable field raises a ValueError.
    """
    @patch("database_manager.mysql.connector.connect")
    def setUp(self, mock_connect):
        """
        Sets up a mock database connection and initializes the `TestDatabaseManagerConcrete` instance.

        This method patches the database connection and mocks the `_update_row` and `get_by_id` methods to avoid actual database interaction.
        """
        self.mock_db_manager = TestDatabaseManagerConcrete(
            host="localhost",
            user="root",
            password="password",
            database="test_db"
        )
        self.mock_db_manager._update_row = MagicMock()

        self.mock_db_manager.get_by_id = MagicMock(return_value={
            "id": "123e4567-e89b-12d3-a456-426614174000",
            "col1": "old_value1",
            "col2": "old_value2",
            "col3": 100.00
        })

    def test_update_non_immutable_field(self):
        """
        Validates updating a non-immutable field (`col3`) on the database record.

        This test checks that attempting to update a mutable field (`col3`) successfully calls `_update_row` without raising errors.
        """
        self.mock_db_manager.update_row("123e4567-e89b-12d3-a456-426614174000", col3=200.00)
        
        self.mock_db_manager._update_row.assert_called_once_with("123e4567-e89b-12d3-a456-426614174000", "id", col3=200.00)

    def test_update_immutable_fiel(self):
        """
        Validates that attempting to update an immutable field (`col1`) raises a ValueError.

        This test confirms that the `immutable_fields` decorator prevents updates to fields specified as immutable
        by raising a `ValueError` and not calling the `_update_row` method.
        """
        with self.assertRaises(ValueError) as context:
            self.mock_db_manager.update_row("123e4567-e89b-12d3-a456-426614174000", col1="new_value")

        self.assertEqual(str(context.exception), "The 'col1' field is immutable and cannot be updated.")

        self.mock_db_manager._update_row.assert_not_called()

if __name__ == "__main__":
    unittest.main()