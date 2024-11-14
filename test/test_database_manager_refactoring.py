import unittest
from unittest.mock import MagicMock, patch
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), 'src')))
from database_manager_refactoring import DatabaseManager, Config


class TestDatabaseManager(unittest.TestCase):

    @patch("database_manager_refactoring.mysql.connector.connect")
    def setUp(self, mock_connect):
        # Mock the MySQL connection and cursor
        self.mock_conn = MagicMock()
        self.mock_cursor = MagicMock()
        mock_connect.return_value = self.mock_conn
        self.mock_conn.cursor.return_value = self.mock_cursor

        # Setup Config and DatabaseManager instance
        config = Config(
            host="localhost",
            user="root",
            password="password",
            database="test_db",
            table_name="test_table",
            columns=["id", "name", "value"],
            column_id="id"
        )
        self.manager = DatabaseManager(config)

    def test_insert_row(self):
        # Test insert row with sample data
        self.manager._insert_row(name="Test Name", value=42)
        self.mock_cursor.execute.assert_called_once()
        sql, params = self.mock_cursor.execute.call_args[0]
        self.assertIn("INSERT INTO `test_table`", sql)
        self.assertEqual(len(params), 3)  # id, name, value

    def test_update_row(self):
        # Test updating a row
        self.manager._update_row(record_id="123", name="Updated Name")
        self.mock_cursor.execute.assert_called_once()
        sql, params = self.mock_cursor.execute.call_args[0]
        self.assertIn("UPDATE `test_table` SET", sql)
        self.assertEqual(params[-1], "123")  # Last param is the record_id
'''
    def test_delete_row(self):
        # Test deleting a row
        self.manager._delete_row("123")
        self.mock_cursor.execute.assert_called_once_with("DELETE FROM `test_table` WHERE `id` = %s;", ("123",))

    def test_get_by_id(self):
        # Set up the cursor to return a specific result
        self.mock_cursor.fetchone.return_value = (123, "Sample Name", 42)
        result = self.manager._get_by_id("123")
        self.mock_cursor.execute.assert_called_once_with("SELECT * FROM `test_table` WHERE `id` = %s;", ("123",))
        self.assertEqual(result, (123, "Sample Name", 42))

    def test_search_record(self):
        # Set up the cursor to return multiple records
        self.mock_cursor.fetchall.return_value = [(1, "First", 42), (2, "Second", 50)]
        result = self.manager._search_record(name="First")
        self.mock_cursor.execute.assert_called_once()
        sql, params = self.mock_cursor.execute.call_args[0]
        self.assertIn("SELECT * FROM `test_table` WHERE `name` = %s;", sql)
        self.assertEqual(result, [(1, "First", 42), (2, "Second", 50)])

    def tearDown(self):
        self.mock_cursor.close.assert_called_once()
        self.mock_conn.close.assert_called_once()
'''

if __name__ == "__main__":
    unittest.main()
