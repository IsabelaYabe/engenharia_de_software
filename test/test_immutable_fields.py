import unittest
from unittest.mock import MagicMock, patch
from flask import Flask, jsonify, request

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), 'src')))
from database_manager import DatabaseManager
from decorators import immutable_fields

class TestDatabaseManagerConcrete(DatabaseManager):
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
    @patch("database_manager.mysql.connector.connect")
    def setUp(self, mock_connect):
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
        self.mock_db_manager.update_row("123e4567-e89b-12d3-a456-426614174000", col3=200.00)
        
        self.mock_db_manager._update_row.assert_called_once_with("123e4567-e89b-12d3-a456-426614174000", "id", col3=200.00)

    def test_update_immutable_fiel(self):
        with self.assertRaises(ValueError) as context:
            self.mock_db_manager.update_row("123e4567-e89b-12d3-a456-426614174000", col1="new_value")

        self.assertEqual(str(context.exception), "The 'col1' field is immutable and cannot be updated.")

        self.mock_db_manager._update_row.assert_not_called()

if __name__ == "__main__":
    unittest.main()