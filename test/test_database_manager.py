"""
    Module for unit testing the DatabaseManager class.

    Author: Isabela Yabe 

    Last Modified: 15/10/2024

    Dependencies: 
        - unittest
        - uuid
        - os
        - sys
        - ProductProfile
        - load_banned_words
        - contains_banned_words
"""

import unittest
from unittest.mock import patch, MagicMock
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), 'src')))
from database_manager import DatabaseManager

class TestDatabaseManager(unittest.TestCase):

    def setUp(self):
        """
        This method is called before each test.
        Initializes a DatabaseManager instance for testing.
        """
        self.db_manager = DatabaseManager("localhost", "root", "password", "test_db", "test_table")

    @patch("mysql.connector.connect")
    def test_connect(self, mock_connect):
        """
        Test if _connect method calls mysql.connector.connect with correct config.
        """
        mock_connection = MagicMock()
        mock_connect.return_value = mock_connection

        conn = self.db_manager._connect()

        mock_connect.assert_called_with(
            host="localhost",
            user="root",
            password="password",
            database="test_db"
        )

        self.assertEqual(conn, mock_connection)

    @patch("mysql.connector.connect")
    def test_create_table(self, mock_connect):
        """
        Test the _create_table method by simulating table creation.
        """
        mock_connection = MagicMock()
        mock_connect.return_value = mock_connection
        mock_cursor = mock_connection.cursor.return_value

        create_table_sql = """
        CREATE TABLE IF NOT EXISTS test_table (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255)
        );
        """

        self.db_manager._create_table(create_table_sql)

        mock_cursor.execute.assert_called_with(create_table_sql)
        mock_connection.commit.assert_called_once()
        mock_cursor.close.assert_called_once()

    @patch("mysql.connector.connect")
    def test_insert_row(self, mock_connect):
        """
        Test the insert_row method by simulating a row insertion.
        """
        mock_connection = MagicMock()
        mock_connect.return_value = mock_connection
        mock_cursor = mock_connection.cursor.return_value

        columns = ["id", "name"]
        values = ("123e4567-e89b-12d3-a456-426614174000", "Product")

        self.db_manager._insert_row(columns, values)

        expected_sql = "INSERT INTO test_table (id, name) VALUES (%s, %s);"
        mock_cursor.execute.assert_called_with(expected_sql, values)
        mock_connection.commit.assert_called_once()
        mock_cursor.close.assert_called_once()

    @patch("mysql.connector.connect")
    def test_modify_column(self, mock_connect):
        """
        Test the modify_column method by simulating a column name change.
        """
        mock_connection = MagicMock()
        mock_connect.return_value = mock_connection
        mock_cursor = mock_connection.cursor.return_value

        self.db_manager._modify_column("old_name", "new_name")

        expected_sql = "ALTER TABLE test_table CHANGE old_name new_name;"
        mock_cursor.execute.assert_called_with(expected_sql)
        mock_connection.commit.assert_called_once()
        mock_cursor.close.assert_called_once()

    @patch("mysql.connector.connect")
    def test_delete_row(self, mock_connect):
        """
        Test the delete_row method by simulating the deletion of a row.
        """
        mock_connection = MagicMock()
        mock_connect.return_value = mock_connection
        mock_cursor = mock_connection.cursor.return_value

        self.db_manager._delete_row("123e4567-e89b-12d3-a456-426614174000")

        expected_sql = "DELETE FROM test_table WHERE id = %s;"

        mock_cursor.execute.assert_called_with(expected_sql, ("123e4567-e89b-12d3-a456-426614174000",))
        mock_connection.commit.assert_called_once()
        mock_cursor.close.assert_called_once()

    @patch("mysql.connector.connect")
    def test_delete_table(self, mock_connect):
        """
        Test the delete_table method by simulating the deletion of the entire table.
        """
        mock_connection = MagicMock()
        mock_connect.return_value = mock_connection
        mock_cursor = mock_connection.cursor.return_value

        self.db_manager._delete_table()

        expected_sql = "DROP TABLE IF EXISTS test_table;"
        mock_cursor.execute.assert_called_with(expected_sql)
        mock_connection.commit.assert_called_once()
        mock_cursor.close.assert_called_once()

    @patch("mysql.connector.connect")
    def test_update_row(self, mock_connect):
        """
        Test the update_row method by simulating updating specific columns in a row.
        """
        # Mock connection and cursor
        mock_connection = MagicMock()
        mock_connect.return_value = mock_connection
        mock_cursor = mock_connection.cursor.return_value
        
        column_values = {"name": "Updated Name", "price": 59.99}
        condition = "id = '123e4567-e89b-12d3-a456-426614174000'"

        self.db_manager._update_row(column_values, condition)

        expected_sql = "UPDATE test_table SET name = %s, price = %s WHERE id = '123e4567-e89b-12d3-a456-426614174000';"

        mock_cursor.execute.assert_called_with(
            expected_sql, 
            ("Updated Name", 59.99)
        )

        mock_connection.commit.assert_called_once()
        mock_cursor.close.assert_called_once()

    @patch("mysql.connector.connect")
    def test_get_by_id(self, mock_connect):
        """
        Test the get_by_id method by simulating a database query.
        """
        mock_connection = MagicMock()
        mock_connect.return_value = mock_connection
        mock_cursor = mock_connection.cursor.return_value

        mock_cursor.fetchone.return_value = ("123e4567-e89b-12d3-a456-426614174000", "Product")

        result = self.db_manager._get_by_id("123e4567-e89b-12d3-a456-426614174000", id_column="product_id")

        expected_result = {
            "product_id": "123e4567-e89b-12d3-a456-426614174000"
        }

        self.assertEqual(result, expected_result)

        mock_cursor.execute.assert_called_with(
            "SELECT * FROM test_table WHERE product_id = %s",  
            ("123e4567-e89b-12d3-a456-426614174000",)
        )

        mock_cursor.close.assert_called_once()
        mock_connection.close.assert_called_once()



if __name__ == "__main__":
    unittest.main()
