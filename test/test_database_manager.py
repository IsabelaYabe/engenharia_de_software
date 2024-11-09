"""
    Module for unit testing the DatabaseManager class.

    Author: Isabela Yabe 

    Last Modified: 06/11/2024

    Dependencies:
        - setup_logger
        - unittest
        - uuid
        - os
        - sys
        - DatabaseManager
        - Flask
        - mysql.connector
"""
import uuid
import unittest
from unittest.mock import patch, MagicMock
from flask import Flask
import mysql.connector
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), 'src')))
from custom_logger import setup_logger
from database_manager import DatabaseManager
from concrete_db_manager import TestDatabaseManagerConcrete

logger = setup_logger()

class TestDatabaseManager(unittest.TestCase):
    def setUp(self):
        logger.info("SetUp module to test")
        self.mock_db_manager = TestDatabaseManagerConcrete(
            host="localhost",
            user="root",
            password="password",
            database="test_db",
            table_name="test_table"
        )
        
        self.mock_db_manager._create_table = MagicMock()
        self.mock_db_manager.insert_row = MagicMock()            
        self.mock_db_manager.update_row = MagicMock()
        self.mock_db_manager.delete_row = MagicMock()
        self.mock_db_manager.get_by_id = MagicMock()

    @patch("database_manager.mysql.connector.connect") 
    def test_connect(self, mock_connect):
        """
        Test if _connect method calls database_manager.mysql.connector.connect with correct config.
        """
        mock_connection = MagicMock()
        mock_connect.return_value = mock_connection 
        conn = self.mock_db_manager._DatabaseManager__connect()

        mock_connect.assert_called_once_with(
            host="localhost",
            user="root",
            password="password",
            database="test_db"
        )

        self.assertTrue(conn)
    
    @patch("database_manager.mysql.connector.connect")
    def test_create_table_(self, mock_connect):
        """
        Test the _create_table_ method by simulating table creation.
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

        self.mock_db_manager._create_table_(create_table_sql)
        mock_connect.assert_called_once_with(
            host="localhost",
            user="root",
            password="password",
            database="test_db"
        )
        mock_cursor.execute.assert_called_once_with(create_table_sql)
        mock_connection.commit.assert_called_once()
        mock_cursor.close.assert_called_once()
    
    @patch("database_manager.mysql.connector.connect")
    def test_modify_column(self, mock_connect):
        """
        Test the modify_column method by simulating a column name change.
        """
        mock_connection = MagicMock()
        mock_connect.return_value = mock_connection
        mock_cursor = mock_connection.cursor.return_value

        expected_sql = f"ALTER TABLE `test_table` RENAME COLUMN `old_column_name` TO `new_column_name`;"

        self.mock_db_manager._modify_column("old_column_name", "new_column_name")

        mock_cursor.execute.assert_called_once_with(expected_sql)
        
        mock_connection.commit.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_connection.close.assert_called_once()
       
    @patch("database_manager.mysql.connector.connect")
    def test_modify_column_duplicate(self, mock_connect):
        """
        Test the modify_column method by simulating a column name duplicate change.
        """
        mock_connection = MagicMock()
        mock_connect.return_value = mock_connection
        mock_cursor = mock_connection.cursor.return_value

        mock_cursor.execute.side_effect = mysql.connector.Error(errno=1060, msg="Duplicate column name.")

        with self.assertRaises(ValueError)as conTest:
            self.mock_db_manager._modify_column("old_name", "existing_column_name")

        self.assertEqual(str(conTest.exception), "Existing column name (`existing_column_name`): Duplicate column name.")
        
        mock_connection.rollback.assert_called_once()
        mock_connection.commit.assert_not_called()
        mock_cursor.close.assert_called_once()
        mock_connection.close.assert_called_once()
    
     
    @patch("database_manager.mysql.connector.connect")
    def test_add_column_not_null_true(self, mock_connect): 
        """
        Test the add_column method by simulation a add column with not null 
        """
        column = "add_col"
        col_type = "VARCHAR(255)"

        mock_connection = MagicMock()
        mock_connect.return_value = mock_connection
        mock_cursor = mock_connection.cursor.return_value

        self.mock_db_manager._add_column(column, col_type, not_null=True)

        expected_sql = f"ALTER TABLE `test_table` ADD `{column}` {col_type} NOT NULL;"
        mock_cursor.execute.assert_called_with(expected_sql)

        mock_connection.commit.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_connection.close.assert_called_once()
    
    @patch("database_manager.mysql.connector.connect")
    def test_add_column_not_null_false(self, mock_connect): 
        """
        Test the add_column method by simulation a add column without not null 
        """
        column = "add_col"
        col_type = "VARCHAR(255)"

        mock_connection = MagicMock()
        mock_connect.return_value = mock_connection
        mock_cursor = mock_connection.cursor.return_value

        self.mock_db_manager._add_column(column, col_type, not_null=False)

        expected_sql = f"ALTER TABLE `test_table` ADD `{column}` {col_type};"
        mock_cursor.execute.assert_called_with(expected_sql)

        mock_connection.commit.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_connection.close.assert_called_once()
    
    @patch("database_manager.mysql.connector.connect")
    def test_add_column_duplicate(self, mock_connect):
        """
        Test the add_column method by simulating a column name duplicate add.
        """
        mock_connection = MagicMock()
        mock_connect.return_value = mock_connection
        mock_cursor = mock_connection.cursor.return_value

        mock_cursor.execute.side_effect = mysql.connector.Error(errno=1060, msg="Duplicate column name.")

        with self.assertRaises(ValueError) as conTest:
            self.mock_db_manager._add_column("existing_column_name", "VARCHAR(255)")

        self.assertEqual(str(conTest.exception), "Existing column name (`existing_column_name`): Duplicate column name.")

        mock_connection.rollback.assert_called_once()
        mock_connection.commit.assert_not_called()
        mock_cursor.close.assert_called_once()
        mock_connection.close.assert_called_once()
    
    @patch("database_manager.mysql.connector.connect")
    def test_delete_column(self, mock_connect): 
        """
        Test the delete_column method by simulation a drop column
        """
        mock_connection = MagicMock()
        mock_connect.return_value = mock_connection
        mock_cursor = mock_connection.cursor.return_value

        self.mock_db_manager._delete_column("drop_col")

        expected_sql = "ALTER TABLE `test_table` DROP COLUMN `drop_col`;"
        mock_cursor.execute.assert_called_with(expected_sql)
        mock_connection.commit.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_connection.close.assert_called_once()
    
    @patch("database_manager.mysql.connector.connect")
    def test_delete_inexistent_column(self, mock_connect):
        """
        Test the delete_column method by simulation a drop inexistent column.
        """
        mock_connection = MagicMock()
        mock_connect.return_value = mock_connection
        mock_cursor = mock_connection.cursor.return_value

        mock_cursor.execute.side_effect = mysql.connector.Error(errno=1054, msg="Column `inexistent_column` not found.")

        with self.assertRaises(ValueError) as conTest:
            self.mock_db_manager._delete_column("inexistent_column")
        
        self.assertEqual(str(conTest.exception), "Column `inexistent_column` not found: Column `inexistent_column` not found.")

        mock_connection.rollback.assert_called_once()
        mock_connection.commit.assert_not_called()
        mock_cursor.close.assert_called_once()
        mock_connection.close.assert_called_once()
    
    @patch("database_manager.mysql.connector.connect")
    def test_delete_row(self, mock_connect):
        """
        Test the delete_row method by simulation a drop row.
        """
        mock_connection = MagicMock()
        mock_connect.return_value = mock_connection
        mock_cursor = mock_connection.cursor.return_value

        expected_sql = "DELETE FROM `test_table` WHERE `column_id` = %s;"

        self.mock_db_manager._delete_row("record_id", "column_id")

        mock_cursor.execute.assert_called_once_with(expected_sql, ("record_id",))
        mock_connection.commit.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_connection.close.assert_called_once()
    
    @patch("database_manager.mysql.connector.connect")
    def test_delete_row_not_found(self, mock_connect):
        """
        Test the delete_row method by simulation a drop not found row.
        """
        mock_connection = MagicMock()
        mock_connect.return_value = mock_connection
        mock_cursor = mock_connection.cursor.return_value

        expected_sql = "DELETE FROM `test_table` WHERE `column_id` = %s;"
        mock_cursor.rowcount = 0

        with patch("builtins.print") as mock_print:
            self.mock_db_manager._delete_row("inexistent_record_id", "column_id")

            mock_print.assert_called_once_with("No rows are deleted; the key was not found.")

        mock_cursor.execute.assert_called_once_with(expected_sql, ("inexistent_record_id",))
        mock_connection.commit.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_connection.close.assert_called_once()

    @patch("database_manager.mysql.connector.connect")
    def test_delete_row_inexistent_column_id(self, mock_connect):
        """
        Test the delete_row method by simulation a drop row with an inexistent column id.
        """

        mock_connection = MagicMock()
        mock_connect.return_value = mock_connection
        mock_cursor = mock_connection.cursor.return_value

        mock_cursor.execute.side_effect = mysql.connector.Error(errno=1054, msg="Unknown column `inexistent_column_id`.")

        with self.assertRaises(ValueError) as conTest:
            self.mock_db_manager._delete_row("record_id", "inexistent_column_id")

        self.assertEqual(str(conTest.exception),"Column `inexistent_column_id` not found: Unknown column `inexistent_column_id`.")

        mock_connection.rollback.assert_called_once()
        mock_connection.commit.assert_not_called()
        mock_connection.close.assert_called_once()
        mock_cursor.close.assert_called_once()

    @patch("database_manager.mysql.connector.connect")
    def test_delete_table(self, mock_connect):
        """
        Test delete_table method by simulation a drop table.
        """
        mock_connection = MagicMock()
        mock_connect.return_value = mock_connection
        mock_cursor = mock_connection.cursor.return_value

        expected_sql = "DROP TABLE IF EXISTS `test_table`;" 

        self.mock_db_manager._delete_table()

        mock_cursor.execute.assert_called_with(expected_sql)
        mock_connection.commit.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_connection.close.assert_called_once()

    @patch("database_manager.mysql.connector.connect")
    def test_insert_row(self, mock_connect):
        """
        Test the insert_row method by simulating a row insertion.
        """
        mock_connection = MagicMock()
        mock_connect.return_value = mock_connection
        mock_cursor = mock_connection.cursor.return_value

        kwargs = {"id": "id_0", "name": "name_0"} 
        self.mock_db_manager._insert_row(**kwargs)

        expected_sql = "INSERT INTO `test_table` (`id`, `name`) VALUES (%s, %s);"
        values = tuple(kwargs.values())
        mock_cursor.execute.assert_called_once_with(expected_sql, values)
        
        mock_connection.commit.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_connection.close.assert_called_once()

    @patch("database_manager.mysql.connector.connect")
    def test_insert_row_incorrect_value_type(self, mock_connect):
        """
        Test the insert_row method by simulating a row insertion with invalid value type.
        """
        mock_connection = MagicMock()
        mock_connect.return_value = mock_connection
        mock_cursor = mock_connection.cursor.return_value

        kwargs = {"id": "id_0", "name": "name_0"} 
        mock_cursor.execute.side_effect = mysql.connector.Error(errno=1366, msg="Incorrect value type.")

        with self.assertRaises(ValueError) as conTest:
            self.mock_db_manager._insert_row(**kwargs)

        self.assertEqual(str(conTest.exception), "Incorrect value type for column: Incorrect value type.")
        
        mock_connection.rollback.assert_called_once()
        mock_connection.commit.assert_not_called()
        mock_connection.close.assert_called_once()
        mock_cursor.close.assert_called_once()
  
    @patch("database_manager.mysql.connector.connect")
    def test_insert_row_missing_value(self, mock_connect):
        """
        Test the insert_row method by simulating a row insertion missing value.
        """
        mock_connection = MagicMock()
        mock_connect.return_value = mock_connection
        mock_cursor = mock_connection.cursor.return_value

        kwargs = {"id": "id_0", "name": "name_0"} 
        mock_cursor.execute.side_effect = mysql.connector.Error(errno=1048, msg="Missing value.")

        with self.assertRaises(ValueError) as conTest:
            self.mock_db_manager._insert_row(**kwargs)

        self.assertEqual(str(conTest.exception), "Missing required value for column: Missing value.")
        
        mock_connection.rollback.assert_called_once()
        mock_connection.commit.assert_not_called()
        mock_connection.close.assert_called_once()
        mock_cursor.close.assert_called_once()

    @patch("database_manager.mysql.connector.connect")
    def test_update_row(self, mock_connect):
        """
        Test update_row method by simulating a update row.
        """
        mock_connection = MagicMock()
        mock_connect.return_value = mock_connection
        mock_cursor = mock_connection.cursor.return_value

        kwargs = {"col_0": "value_0", "col_1": "value_1", "col_2": "value_2"}
        self.mock_db_manager._update_row("record_id", "column_id", **kwargs)

        expected_sql = "UPDATE `test_table` SET `col_0` = %s, `col_1` = %s, `col_2` = %s WHERE `column_id` = %s;"
        values = list(kwargs.values())
        values.append("record_id")
        values = tuple(values)
        mock_cursor.execute.assert_called_once_with(expected_sql, values)

        mock_connection.commit.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_connection.close.assert_called_once()
  
    @patch("database_manager.mysql.connector.connect")
    def test_update_row_inexistent_column_id(self, mock_connect):
        """
        Test update_row method by simulating a update row with inexistent column id.
        """
        mock_connection = MagicMock()
        mock_connect.return_value = mock_connection
        mock_cursor = mock_connection.cursor.return_value

        kwargs = {"col_0": "value_0", "col_1": "value_1", "col_2": "value_2"}
        mock_cursor.execute.side_effect = mysql.connector.Error(errno = 1054, msg="Column not found.")

        with self.assertRaises(ValueError) as contest: 
            self.mock_db_manager._update_row("record_id", "column_id", **kwargs)

        self.assertEqual(str(contest.exception), "Column `column_id` not found: Column not found.")

        mock_connection.commit.assert_not_called()
        mock_connection.rollback.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_connection.close.assert_called_once()

    @patch("database_manager.mysql.connector.connect")
    def test_update_row_missing_value(self, mock_connect): 
        """
        Test update_row method by simulating a update row with missing_value
        """
        mock_connection = MagicMock()
        mock_connect.return_value = mock_connection
        mock_cursor = mock_connection.cursor.return_value

        kwargs = {"col_0": "value_0", "col_1": "value_1", "col_2": None}
        mock_cursor.execute.side_effect = mysql.connector.Error(errno=1048, msg="Missing value.")

        with self.assertRaises(ValueError) as conTest:
            self.mock_db_manager._update_row("record_id", "column_id", **kwargs)

        self.assertEqual(str(conTest.exception), "Missing required value for column: Missing value.")

        mock_connection.commit.assert_not_called()
        mock_connection.rollback.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_connection.close.assert_called_once()

    @patch("database_manager.mysql.connector.connect")
    def test_update_row_incorrect_value_type(self, mock_connect):
        """
        Test update_row method by simulating a update row with incorrect value type for column. 
        """
        mock_connection = MagicMock()
        mock_connect.return_value = mock_connection
        mock_cursor = mock_connection.cursor.return_value

        kwargs = {"col_0": "value_0", "col_1": "value_1", "col_2": 000}
        mock_cursor.execute.side_effect = mysql.connector.Error(errno=1366, msg="Incorrect value type.")

        with self.assertRaises(ValueError) as conTest:
            self.mock_db_manager._update_row("record_id", "column_id", **kwargs)

        self.assertEqual(str(conTest.exception), "Incorrect value type for column: Incorrect value type.")    

        
        mock_connection.commit.assert_not_called()
        mock_connection.rollback.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_connection.close.assert_called_once()

    @patch("database_manager.mysql.connector.connect")
    def test_get_by_id(self, mock_connect):
        """
        Test the get_by_id method by simulating a database query.
        """
        mock_connection = MagicMock()
        mock_connect.return_value = mock_connection
        mock_cursor = mock_connection.cursor.return_value

        mock_cursor.fetchone.return_value = ("instance_id", "instance_value_0", "instance_value_1")

        result = self.mock_db_manager._get_by_id("instance_id", "column_id")

        expected_result = ("instance_id", "instance_value_0", "instance_value_1")

        self.assertEqual(result, expected_result)

        mock_cursor.execute.assert_called_with(
            "SELECT * FROM `test_table` WHERE `column_id` = %s;",  
            ("instance_id",)
        )

        mock_cursor.close.assert_called_once()
        mock_connection.close.assert_called_once()
   
    @patch("database_manager.mysql.connector.connect")
    def test_get_by_id_inexistent_column_id(self, mock_connect):
        """
        Test the get_by_id method by simulating a database query with inexistent column id.
        """

        mock_connection = MagicMock()
        mock_connect.return_value = mock_connection
        mock_cursor = mock_connection.cursor.return_value

        mock_cursor.execute.side_effect = mysql.connector.Error(errno=1054, msg="Column not found.")

        with self.assertRaises(ValueError) as conTest: 
            self.mock_db_manager._get_by_id("instance_id", "column_id")

        self.assertEqual(str(conTest.exception), "Column `column_id` not found: Column not found.")

        mock_connection.rollback.assert_called_once()
        mock_connection.commit.assert_not_called()
        mock_cursor.close.assert_called_once()
        mock_connection.close.assert_called_once()

    @patch("database_manager.mysql.connector.connect")
    def test_rollback(self, mock_connect):
        """
        Test the rollback method by a simulating an uncommitted transaction. 
        """
        mock_connection = MagicMock()
        mock_connect.return_value = mock_connection

        self.mock_db_manager._rollback(mock_connection)
        
        mock_connection.rollback.assert_called_once()

    @patch("database_manager.mysql.connector.connect")
    def test_execute_sql(self, mock_connect):
        """
        Test the execute_sql method by simulating a query.
        """
        mock_connection = MagicMock()
        mock_connect.return_value = mock_connection
        mock_cursor = mock_connection.cursor.return_value

        expected_sql = "SELECT * FROM test_table;"

        result = self.mock_db_manager._execute_sql(expected_sql)

        mock_cursor.execute.assert_called_once_with(expected_sql, None)
        mock_connection.commit.assert_called_once()
        
        self.assertIsNone(result)

        mock_cursor.close.assert_called_once()
        mock_connection.close.assert_called_once()

    @patch("database_manager.mysql.connector.connect")
    def test_execute_sql_fetch_one(self, mock_connect):
        """
        Test the execute_sql method by simulating a query with fetchone.
        """
        mock_connection = MagicMock()
        mock_connect.return_value = mock_connection
        mock_cursor = mock_connection.cursor.return_value
        mock_cursor.fetchone.return_value = ("result",)

        expected_sql = "SELECT * FROM test_table WHERE `col 1` = 1;"
        
        result = self.mock_db_manager._execute_sql(expected_sql, fetch_one=True)

        mock_cursor.execute.assert_called_once_with(expected_sql, None)
        self.assertEqual(result, ("result",))
        mock_cursor.close.assert_called_once()
        mock_connection.close.assert_called_once()

    @patch("database_manager.mysql.connector.connect")
    def test_execute_sql_error(self, mock_connect):
        """
        Test the execute_sql method by simulating a query with error.
        """
        mock_connection = MagicMock()
        mock_connect.return_value = mock_connection
        mock_cursor = mock_connection.cursor.return_value

        query = "ALTER TABLE test_table ADD column_name;" 
        msg = "Duplicate column name"

        mock_cursor.execute.side_effect = mysql.connector.Error(errno= 1060, msg="Error executing query")

        with self.assertRaises(ValueError) as conTest:
            self.mock_db_manager._execute_sql(query, error_message=msg)

        self.assertEqual(str(conTest.exception), "Duplicate column name: Error executing query (errno=1060)")

        mock_connection.rollback.assert_called_once()
        mock_connection.commit.assert_not_called()
        mock_cursor.close.assert_called_once()
        mock_connection.close.assert_called_once()

if __name__ == "__main__":
    unittest.main()