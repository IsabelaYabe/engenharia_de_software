import unittest
from unittest.mock import MagicMock, patch
import re
import mysql.connector
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), 'src')))
from database_manager_refactoring import DatabaseManager, Config
from custom_logger import setup_logger
logger = setup_logger()

class TestDatabaseManager(unittest.TestCase):
    
    def setUp(self):
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

    @patch("database_manager_refactoring.mysql.connector.connect")
    def test_connect(self, mock_connect):
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
        logger.info("Test connect: OK!!! ---------------------------> TESTE 1 OK!!!")
    
    @patch("database_manager_refactoring.mysql.connector.connect")
    def test_modify_column_success(self, mock_connect):
        mock_connection = MagicMock()
        mock_connect.return_value = mock_connection
        # Change de enviroment (with)
        mock_connection = mock_connection.__enter__()
        mock_cursor = mock_connection.cursor().__enter__.return_value
        
        expected_sql = "ALTER TABLE `test_table` RENAME COLUMN `col1` TO `col0`;"
        self.db_manager._modify_column("col1", "col0")

        mock_cursor.execute.assert_called_once_with(expected_sql)
        self.assertEqual(["id", "col0", "col2", "col3"], self.  db_manager.columns)
        logger.info("Test modify column sucess: OK!!! ---------------------------> TESTE 2 OK!!!")

    def test_modify_column_modify_column_id_error(self):
        with self.assertRaises(ValueError) as context:
            self.db_manager._modify_column("id", "new_column_id")
        
        self.assertEqual(str(context.exception), "You can't modify an id column!")
        self.assertEqual(["id", "col1", "col2", "col3"], self.db_manager.columns)
        logger.info("Test modify column column id error: OK!!! ---------------------------> TESTE 3 OK!!!")

    @patch("database_manager_refactoring.mysql.connector.connect")
    def test_add_column_not_null_true(self, mock_connect):
        mock_connection = MagicMock()
        mock_connect.return_value = mock_connection
        # Change de enviroment (with)
        mock_connection = mock_connection.__enter__()
        mock_cursor = mock_connection.cursor().__enter__.return_value

        expected_sql = "ALTER TABLE `test_table` ADD `new_col` INT NOT NULL;"
        self.db_manager._add_column("new_col", "INT")
        
        mock_cursor.execute.assert_called_once_with(expected_sql)
        self.assertEqual(["id", "col1", "col2", "col3", "new_col"], self.db_manager.columns)
        logger.info("Test add column column not null true: OK!!! ---------------------------> TESTE 4 OK!!!")

    @patch("database_manager_refactoring.mysql.connector.connect")
    def test_add_column_not_null_false(self, mock_connect):
        mock_connection = MagicMock()
        mock_connect.return_value = mock_connection
        # Change de enviroment (with)
        mock_connection = mock_connection.__enter__()
        mock_cursor = mock_connection.cursor().__enter__.return_value

        expected_sql = "ALTER TABLE `test_table` ADD `new_col` INT;"
        self.db_manager._add_column("new_col", "INT", not_null=False)
        
        mock_cursor.execute.assert_called_once_with(expected_sql)
        self.assertEqual(["id", "col1", "col2", "col3", "new_col"], self.db_manager.columns)
        logger.info("Test add column column not null false: OK!!! ---------------------------> TESTE 5 OK!!!")

    @patch("database_manager_refactoring.mysql.connector.connect")
    def test_delete_column(self, mock_connect):
        mock_connection = MagicMock()
        mock_connect.return_value = mock_connection
        # Change de enviroment (with)
        mock_connection = mock_connection.__enter__()
        mock_cursor = mock_connection.cursor().__enter__.return_value

        expected_sql = "ALTER TABLE `test_table` DROP COLUMN `col2`;"
        self.db_manager._delete_column("col2")

        mock_cursor.execute.assert_called_once_with(expected_sql)
        self.assertEqual(["id", "col1", "col3"], self.db_manager.columns)
        logger.info("Test delete column: OK!!! ---------------------------> TESTE 6 OK!!!")

    @patch("database_manager_refactoring.mysql.connector.connect")
    def test_delete_rows(self, mock_connect):
        mock_connection = MagicMock()
        mock_connect.return_value = mock_connection
        # Change de enviroment (with)
        mock_connection = mock_connection.__enter__()
        mock_cursor = mock_connection.cursor().__enter__.return_value
        mock_cursor.rowcount.return_value = 1
        
        expected_sql = "DELETE FROM `test_table` WHERE `col1` = %s;"
        self.db_manager._delete_rows("record", "col1")

        mock_cursor.execute.assert_called_once_with(expected_sql, ("record",))
        logger.info("Test delete rows: OK!!! ---------------------------> TESTE 7 OK!!!")
    
    @patch("database_manager_refactoring.mysql.connector.connect")
    def test_delete_rows_not_found(self, mock_connect):
        mock_connection = MagicMock()
        mock_connect.return_value = mock_connection
        # Change de enviroment (with)
        mock_connection = mock_connection.__enter__()
        mock_cursor = mock_connection.cursor().__enter__.return_value
        mock_cursor.rowcount.return_value = 0

        expected_sql = "DELETE FROM `test_table` WHERE `col1` = %s;"
        self.db_manager._delete_rows("record", "col1")

        mock_cursor.execute.assert_called_once_with(expected_sql, ("record",))
        logger.info("Test delete rows not found: OK!!! ---------------------------> TESTE 8 OK!!!")
    
    def test_regex_to_get_table_name(self):
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
        logger.info("Test regex to get table name: OK!!! ---------------------------> TESTE 9 OK!!!")
    
    @patch("database_manager_refactoring.mysql.connector.connect")
    def test_create_non_exist_table(self, mock_connect):
        mock_connection = MagicMock()
        mock_connect.return_value = mock_connection
        # Change de enviroment (with)
        mock_connection = mock_connection.__enter__()
        mock_cursor = mock_connection.cursor().__enter__.return_value

        check_table_sql = """
                    SELECT * FROM INFORMATION_SCHEMA.TABLES
                    WHERE TABLE_SCHEMA = %s
                    AND TABLE_NAME =  %s;
                    """
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

        self.db_manager._create_table(expected_sql)

        mock_cursor.execute.assert_any_call(
                    """
                    SELECT * FROM INFORMATION_SCHEMA.TABLES
                    WHERE TABLE_SCHEMA = %s
                    AND TABLE_NAME =  %s;
                    """,
                    ("test_db","test_table"))
        mock_cursor.execute.assert_any_call(expected_sql)
        logger.info("Test create non exist table: OK!!! ---------------------------> TESTE 10 OK!!!")
    
    @patch("database_manager_refactoring.mysql.connector.connect")
    def algo(self, mock_connect):
        mock_connection = MagicMock()
        mock_connect.return_value = mock_connection
        # Change de enviroment (with)
        mock_connection = mock_connection.__enter__()
        mock_cursor = mock_connection.cursor().__enter__.return_value

if __name__ == "__main__":
    unittest.main()