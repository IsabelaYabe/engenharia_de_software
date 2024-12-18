
"""
Module for Testing DatabaseManager Class.

This module provides a suite of unit tests for the `DatabaseManager` class using the `unittest` framework.
It tests various operations such as table management, CRUD operations, and custom functionalities like
SQL execution and column modifications.

Author: Isabela Yabe
Last Modified: 19/11/2024
Status: Complete

Dependencies:
    - unittest
    - unittest.mock
    - res
    - uuid
    - custom_logger.setup_logger
    - database_manager.DatabaseManager
"""

import unittest
from unittest.mock import MagicMock, patch
import re
import uuid
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), 'src')))
from database_manager import DatabaseManager, Config
from custom_logger import setup_logger

logger = setup_logger()

class TestDatabaseManager(unittest.TestCase):
    """
    TestDatabaseManager class.

    This class provides unit tests for the `DatabaseManager` class, focusing on its ability to manage MySQL database
    tables, perform CRUD operations, and handle various edge cases and error conditions.
    """
    
    def setUp(self):
        """
        Set up the test environment before each test case.
        """
        config = Config(
            host="localhost",
            user="root",
            password="password",
            database="test_db",
            table_name="test_table",
            columns=["id", "col1", "col2", "col3"],
            column_id="id"
        )
        
        self.db_manager = DatabaseManager(config)

    @patch("database_manager.mysql.connector.connect")
    def test_connect(self, mock_connect):
        """
        Test the connection to the MySQL database.
        """
        mock_connection = MagicMock()
        mock_connect.return_value = mock_connection

        conn = self.db_manager._DatabaseManager__connect()
        
        mock_connect.assert_called_once_with(
            host="localhost",
            user="root",
            password="password",
            database="test_db"
        )

        self.assertTrue(conn)
        logger.info("Test connect: OK!!! ---------------------------> TEST 1 OK!!!")
    
    @patch("database_manager.mysql.connector.connect")
    def test_modify_column_success(self, mock_connect):
        """
        Test the modification of a column in the database table.
        """
        mock_connection = MagicMock()
        mock_connect.return_value = mock_connection
        # Change de enviroment (with)
        mock_connection = mock_connection.__enter__()
        mock_cursor = mock_connection.cursor().__enter__.return_value
        
        expected_sql = "ALTER TABLE `test_table` RENAME COLUMN `col1` TO `col0`;"
        self.db_manager.modify_column("col1", "col0")

        mock_cursor.execute.assert_called_once_with(expected_sql)
        self.assertEqual(["id", "col0", "col2", "col3"], self.  db_manager.columns)
        logger.info("Test modify column sucess: OK!!! ---------------------------> TEST 2 OK!!!")

    def test_modify_column_modify_column_id_error(self):
        """
        Test that modifying the id column raises a ValueError.
        """
        with self.assertRaises(ValueError) as context:
            self.db_manager.modify_column("id", "new_column_id")
        
        self.assertEqual(str(context.exception), "You can't modify an id column!")
        self.assertEqual(["id", "col1", "col2", "col3"], self.db_manager.columns)
        logger.info("Test modify column column id error: OK!!! ---------------------------> TEST 3 OK!!!")

    @patch("database_manager.mysql.connector.connect")
    def test_add_column_not_null_true(self, mock_connect):
        """
        Test adding a new column to the database table with the NOT NULL constraint
        """
        mock_connection = MagicMock()
        mock_connect.return_value = mock_connection
        # Change de enviroment (with)
        mock_connection = mock_connection.__enter__()
        mock_cursor = mock_connection.cursor().__enter__.return_value

        expected_sql = "ALTER TABLE `test_table` ADD `new_col` INT NOT NULL;"
        self.db_manager.add_column("new_col", "INT")
        
        mock_cursor.execute.assert_called_once_with(expected_sql)
        self.assertEqual(["id", "col1", "col2", "col3", "new_col"], self.db_manager.columns)
        logger.info("Test add column column not null true: OK!!! ---------------------------> TEST 4 OK!!!")

    @patch("database_manager.mysql.connector.connect")
    def test_add_column_not_null_false(self, mock_connect):
        """
        Test adding a new column to the database table without the NOT NULL constraint
        """
        mock_connection = MagicMock()
        mock_connect.return_value = mock_connection
        # Change de enviroment (with)
        mock_connection = mock_connection.__enter__()
        mock_cursor = mock_connection.cursor().__enter__.return_value

        expected_sql = "ALTER TABLE `test_table` ADD `new_col` INT;"
        self.db_manager.add_column("new_col", "INT", not_null=False)
        
        mock_cursor.execute.assert_called_once_with(expected_sql)
        self.assertEqual(["id", "col1", "col2", "col3", "new_col"], self.db_manager.columns)
        logger.info("Test add column column not null false: OK!!! ---------------------------> TEST 5 OK!!!")

    @patch("database_manager.mysql.connector.connect")
    def test_delete_column(self, mock_connect):
        """
        Test deleting a column from the database table.
        """
        mock_connection = MagicMock()
        mock_connect.return_value = mock_connection
        # Change de enviroment (with)
        mock_connection = mock_connection.__enter__()
        mock_cursor = mock_connection.cursor().__enter__.return_value

        expected_sql = "ALTER TABLE `test_table` DROP COLUMN `col2`;"
        self.db_manager.delete_column("col2")

        mock_cursor.execute.assert_called_once_with(expected_sql)
        self.assertEqual(["id", "col1", "col3"], self.db_manager.columns)
        logger.info("Test delete column: OK!!! ---------------------------> TEST 6 OK!!!")
        
    @patch("database_manager.DatabaseManager.search_record")
    @patch("database_manager.mysql.connector.connect")
    def test_delete_rows(self, mock_connect, mock_search_record):
        """
        Test deleting rows from the database table.
        """
        mock_connection = MagicMock()
        mock_connect.return_value = mock_connection
        # Change de enviroment (with)
        mock_connection = mock_connection.__enter__()
        mock_cursor = mock_connection.cursor().__enter__.return_value
        mock_cursor.rowcount.return_value = 1
    
        mock_search_record.return_value = [("id_1", "record", "value_21", "value_31"), ("id_2", "record", "value_22", "value_32")]
        
        expected_sql = "DELETE FROM `test_table` WHERE `col1` = %s;"
        self.db_manager.delete_rows("record", "col1")

        mock_cursor.execute.assert_any_call(expected_sql, ("record",))
        logger.info("Test delete rows: OK!!! ---------------------------> TEST 7 OK!!!")
    
    @patch("database_manager.mysql.connector.connect")
    def test_delete_rows_not_found(self, mock_connect):
        """
        Test deleting rows from the database table when no rows are found.
        """
        mock_connection = MagicMock()
        mock_connect.return_value = mock_connection
        # Change de enviroment (with)
        mock_connection = mock_connection.__enter__()
        mock_cursor = mock_connection.cursor().__enter__.return_value
        mock_cursor.rowcount.return_value = 0

        expected_sql = "DELETE FROM `test_table` WHERE `col1` = %s;"
        self.db_manager.delete_rows("record", "col1")

        mock_cursor.execute.assert_any_call(expected_sql, ("record",))
        logger.info("Test delete rows not found: OK!!! ---------------------------> TEST 8 OK!!!")
    
    def test_regex_to_get_table_name(self):
        """
        Test the regex pattern to extract the table name from a CREATE TABLE SQL query.
        """
        sql_query_1 = """
        CREATE TABLE `test_table` (
            id VARCHAR(36) PRIMARY KEY,
            col1 VARCHAR(255) NOT NULL
        );
        """
        sql_query_2 = """
        CREATE TABLE test_table (
            id VARCHAR(36) PRIMARY KEY,
            col1 VARCHAR(255) NOT NULL
        );
        """
        regex = r"CREATE TABLE\s`?+([a-zA-Z0-9_]+)`?\s*\("
        match_1 = re.search(regex, sql_query_1, re.IGNORECASE)
        table_name_1 = match_1.group(1)
        self.assertEqual(table_name_1, "test_table")

        match_2 = re.search(regex, sql_query_2, re.IGNORECASE)
        table_name_2 = match_2.group(1)
        self.assertEqual(table_name_2, "test_table")
        logger.info("Test regex to get table name: OK!!! ---------------------------> TEST 9 OK!!!")
    
    @patch("database_manager.mysql.connector.connect")
    def test_create_non_exist_table(self, mock_connect):
        """
        Test creating a new table in the database when the table does not exist.
        """
        mock_connection = MagicMock()
        mock_connect.return_value = mock_connection
        # Change de enviroment (with)
        mock_connection = mock_connection.__enter__()
        mock_cursor = mock_connection.cursor().__enter__.return_value

        expected_sql = """
        CREATE TABLE `test_table` (
            id VARCHAR(36) PRIMARY KEY,
            col1 VARCHAR(255) NOT NULL,
            col2 TEXT,
            col3 DECIMAL(10, 2) NOT NULL,
            col4 INT NOT NULL
        );
        """
        mock_cursor.fetchone.return_value = [0]

        self.db_manager.create_table(expected_sql)

        mock_cursor.execute.assert_any_call("""
                    SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES
                    WHERE TABLE_SCHEMA = %s
                    AND TABLE_NAME =  %s;
                    """,
                    ("test_db","test_table"))
        mock_cursor.execute.assert_any_call(expected_sql)
        logger.info("Test create non exist table: OK!!! ---------------------------> TEST 10 OK!!!")

    @patch("database_manager.mysql.connector.connect")
    def test_create_exist_table(self, mock_connect):
        """
        Test creating a new table in the database when the table already exists.
        """
        mock_connection = MagicMock()
        mock_connect.return_value = mock_connection
        # Change de enviroment (with)
        mock_connection = mock_connection.__enter__()
        mock_cursor = mock_connection.cursor().__enter__.return_value

        expected_sql = """
        CREATE TABLE `test_table` (
            id VARCHAR(36) PRIMARY KEY,
            col1 VARCHAR(255) NOT NULL,
            col2 TEXT,
            col3 DECIMAL(10, 2) NOT NULL,
            col4 INT NOT NULL
        );
        """
        mock_cursor.fetchone.return_value = [1]

        with self.assertRaises(ValueError) as context:
            self.db_manager.create_table(expected_sql)
        
        self.assertEqual(str(context.exception), "This table exist")

        mock_cursor.execute.assert_called_once_with("""
                    SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES
                    WHERE TABLE_SCHEMA = %s
                    AND TABLE_NAME =  %s;
                    """,
                    ("test_db","test_table"))
        logger.info("Test create exist table: OK!!! ---------------------------> TEST 11 OK!!!")

    @patch("database_manager.mysql.connector.connect")
    def test_delete_table(self, mock_connect):
        """
        Test deleting a table from the database.
        """
        mock_connection = MagicMock()
        mock_connect.return_value = mock_connection
        # Change de enviroment (with)
        mock_connection = mock_connection.__enter__()
        mock_cursor = mock_connection.cursor().__enter__.return_value

        self.db_manager.delete_table()

        mock_cursor.execute.assert_called_once_with("DROP TABLE IF EXISTS `test_table`;")
        logger.info("Test delete table: OK!!! ---------------------------> TEST 12 OK!!!")

    
    @patch("database_manager.mysql.connector.connect")
    def test_update_row(self, mock_connect):
        """
        Test updating a row in the database table.
        """
        mock_connection = MagicMock()
        mock_connect.return_value = mock_connection
        # Change de enviroment (with)
        mock_connection = mock_connection.__enter__()
        mock_cursor = mock_connection.cursor().__enter__.return_value

        record_id = "12345678-1234-5678-1234-567812345678"

        kwargs = {"col0": "value_0", "col_1": "value_1", "col3": "value_3"}

        arguments = []
        values = []
        for key, value in kwargs.items():
            arguments.append(f"`{key}` = %s")
            values.append(value)
        arguments =  ", ".join(arguments)
        values.append(record_id)
        expected_sql = f"UPDATE `test_table` SET {arguments} WHERE `id` = %s;"
        hidden_sql = "SELECT * FROM `test_table` WHERE `id` = %s;"
        
        self.db_manager.update_row(record_id, col0 = "value_0", col_1="value_1", col3= "value_3")

        mock_cursor.execute.assert_any_call(hidden_sql, (record_id,))
        mock_cursor.execute.assert_any_call(expected_sql, tuple(values))
        logger.info("Test update row: OK!!! ---------------------------> TEST 13 OK!!!")
    
    @patch("database_manager.mysql.connector.connect")
    def test_get_by_id(self, mock_connect):
        """
        Test retrieving a row from the database table by ID.
        """
        mock_connection = MagicMock()
        mock_connect.return_value = mock_connection
        # Change de enviroment (with)
        mock_connection = mock_connection.__enter__()
        mock_cursor = mock_connection.cursor().__enter__.return_value

        id = "12345678-1234-5678-1234-567812345678"
        fetchall_return = [(id, "value_1", "value_2", "value_3")] 
        mock_cursor.fetchall.return_value = fetchall_return

        expected_sql = "SELECT * FROM `test_table` WHERE `id` = %s;"

        return_ = self.db_manager.get_by_id("12345678-1234-5678-1234-567812345678")
    
        mock_cursor.execute.assert_called_once_with(expected_sql, (id,))
        mock_cursor.fetchall.assert_called_once()

        self.assertEqual(return_, (id, "value_1", "value_2", "value_3"))                           
        logger.info("Test get by id: OK!!! ---------------------------> TEST 14 OK!!!")

    @patch("database_manager.mysql.connector.connect")
    def test_get_by_id_not_found(self, mock_connect):
        """
        Test retrieving a row from the database table by ID when the row is not found.
        """
        mock_connection = MagicMock()
        mock_connect.return_value = mock_connection
        # Change de enviroment (with)
        mock_connection = mock_connection.__enter__()
        mock_cursor = mock_connection.cursor().__enter__.return_value

        id = "12345678-1234-5678-1234-567812345678"
        fetchall_return = [] 
        mock_cursor.fetchall.return_value = fetchall_return

        expected_sql = "SELECT * FROM `test_table` WHERE `id` = %s;"

        return_ = self.db_manager.get_by_id("12345678-1234-5678-1234-567812345678")
    
        mock_cursor.execute.assert_called_once_with(expected_sql, (id,))
        mock_cursor.fetchall.assert_called_once()
                           
        logger.info("Test get by id not: OK!!! ---------------------------> TEST 15 OK!!!")

    

    @patch("database_manager.mysql.connector.connect")
    def test_execute_sql(self, mock_connect):
        """
        Test executing a custom SQL query on the database.
        """
        mock_connection = MagicMock()
        mock_connect.return_value = mock_connection
        # Change de enviroment (with)
        mock_connection = mock_connection.__enter__()
        mock_cursor = mock_connection.cursor().__enter__.return_value

        expected_sql = "ALTER TABLE `test_table` RENAME COLUMN `col1` TO `col0`;"

        self.db_manager.execute_sql(expected_sql)

        mock_cursor.execute.assert_called_once_with(expected_sql, None)
                               
        logger.info("Test execute sql: OK!!! ---------------------------> TEST 16 OK!!!")

if __name__ == "__main__":
    unittest.main()