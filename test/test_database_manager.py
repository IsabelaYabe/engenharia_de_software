import unittest
from unittest.mock import MagicMock, patch
import re
import mysql.connector
import uuid
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), 'src')))
from database_manager import DatabaseManager, Config
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

    @patch("database_manager.mysql.connector.connect")
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
        logger.info("Test connect: OK!!! ---------------------------> TEST 1 OK!!!")
    
    @patch("database_manager.mysql.connector.connect")
    def test_modify_column_success(self, mock_connect):
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
        with self.assertRaises(ValueError) as context:
            self.db_manager.modify_column("id", "new_column_id")
        
        self.assertEqual(str(context.exception), "You can't modify an id column!")
        self.assertEqual(["id", "col1", "col2", "col3"], self.db_manager.columns)
        logger.info("Test modify column column id error: OK!!! ---------------------------> TEST 3 OK!!!")

    @patch("database_manager.mysql.connector.connect")
    def test_add_column_not_null_true(self, mock_connect):
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

    @patch("database_manager.mysql.connector.connect")
    def test_delete_rows(self, mock_connect):
        mock_connection = MagicMock()
        mock_connect.return_value = mock_connection
        # Change de enviroment (with)
        mock_connection = mock_connection.__enter__()
        mock_cursor = mock_connection.cursor().__enter__.return_value
        mock_cursor.rowcount.return_value = 1
        
        expected_sql = "DELETE FROM `test_table` WHERE `col1` = %s;"
        self.db_manager.delete_rows("record", "col1")

        mock_cursor.execute.assert_called_once_with(expected_sql, ("record",))
        logger.info("Test delete rows: OK!!! ---------------------------> TEST 7 OK!!!")
    
    @patch("database_manager.mysql.connector.connect")
    def test_delete_rows_not_found(self, mock_connect):
        mock_connection = MagicMock()
        mock_connect.return_value = mock_connection
        # Change de enviroment (with)
        mock_connection = mock_connection.__enter__()
        mock_cursor = mock_connection.cursor().__enter__.return_value
        mock_cursor.rowcount.return_value = 0

        expected_sql = "DELETE FROM `test_table` WHERE `col1` = %s;"
        self.db_manager.delete_rows("record", "col1")

        mock_cursor.execute.assert_called_once_with(expected_sql, ("record",))
        logger.info("Test delete rows not found: OK!!! ---------------------------> TEST 8 OK!!!")
    
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
        logger.info("Test regex to get table name: OK!!! ---------------------------> TEST 9 OK!!!")
    
    @patch("database_manager.mysql.connector.connect")
    def test_create_non_exist_table(self, mock_connect):
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
        mock_connection = MagicMock()
        mock_connect.return_value = mock_connection
        # Change de enviroment (with)
        mock_connection = mock_connection.__enter__()
        mock_cursor = mock_connection.cursor().__enter__.return_value

        self.db_manager.delete_table()

        mock_cursor.execute.assert_called_once_with("DROP TABLE IF EXISTS `test_table`;")
        logger.info("Test delete table: OK!!! ---------------------------> TEST 12 OK!!!")

    @patch("uuid.uuid4")
    @patch("database_manager.mysql.connector.connect")
    def test_insert_row(self, mock_connect, mock_uuid):
        id = "12345678-1234-5678-1234-567812345678"
        mock_uuid.return_value = uuid.UUID(id)

        mock_connection = MagicMock()
        mock_connect.return_value = mock_connection
        # Change de enviroment (with)
        mock_connection = mock_connection.__enter__()
        mock_cursor = mock_connection.cursor().__enter__.return_value

        kwargs = {"col0": "value_0", "col_1": "value_1", "col3": "value_3"}

        columns = ["id"]
        values = [id]
        placeholders = []
        for key, value in kwargs.items():
            columns.append(f"`{key}`")
            values.append(value)
            placeholders.append("%s")
        columns_str = ", ".join(columns)
        placeholders = ", ".join(placeholders)

        expected_sql = f"INSERT INTO `test_table` ({columns_str}) VALUES ({placeholders});"
        id_insert_row = self.db_manager.insert_row(col0 = "value_0", col_1="value_1", col3= "value_3")

        mock_cursor.execute.assert_called_once_with(expected_sql, tuple(values))
        self.assertEqual(id_insert_row, id)
        logger.info("Test delete table: OK!!! ---------------------------> TEST 13 OK!!!")
    
    @patch("database_manager.mysql.connector.connect")
    def test_update_row(self, mock_connect):
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
        logger.info("Test update row: OK!!! ---------------------------> TEST 14 OK!!!")
    
    @patch("database_manager.mysql.connector.connect")
    def test_get_by_id(self, mock_connect):
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
        logger.info("Test get by id: OK!!! ---------------------------> TEST 15 OK!!!")

    @patch("database_manager.mysql.connector.connect")
    def test_get_by_id_not_found(self, mock_connect):
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
                           
        logger.info("Test get by id not: OK!!! ---------------------------> TEST 16 OK!!!")

    @patch("database_manager.mysql.connector.connect")
    def test_search_record(self, mock_connect):
        mock_connection = MagicMock()
        mock_connect.return_value = mock_connection
        # Change de enviroment (with)
        mock_connection = mock_connection.__enter__()
        mock_cursor = mock_connection.cursor().__enter__.return_value

        id_1 = "12345678-1234-5678-1234-567812344582"
        id_2 = "85445678-1963-5458-7829-716812340354"
        fetchall_return = [(id_1, "value_1", "value_2", "value_30"), (id_2, "value_1", "value_2", "value_31")] 
        mock_cursor.fetchall.return_value = fetchall_return

        kwargs = {"col1": "value1", "col2": "value2"}
        columns = []
        values = []
        for key, value in kwargs.items():
            columns.append(f"`{key}` = %s")
            values.append(value)
        columns_query = " AND ".join(columns)

        expected_sql = f"SELECT * FROM `test_table` WHERE {columns_query};"

        return_ = self.db_manager.search_record(col1="value1", col2="value2")
    
        mock_cursor.execute.assert_called_once_with(expected_sql, tuple(values))
        mock_cursor.fetchall.assert_called_once()

        self.assertEqual(return_, fetchall_return)                           
        logger.info("Test search record: OK!!! ---------------------------> TEST 17 OK!!!")

    @patch("database_manager.mysql.connector.connect")
    def test_execute_sql(self, mock_connect):
        mock_connection = MagicMock()
        mock_connect.return_value = mock_connection
        # Change de enviroment (with)
        mock_connection = mock_connection.__enter__()
        mock_cursor = mock_connection.cursor().__enter__.return_value

        expected_sql = "ALTER TABLE `test_table` RENAME COLUMN `col1` TO `col0`;"

        self.db_manager.execute_sql(expected_sql)

        mock_cursor.execute.assert_called_once_with(expected_sql, None)
                               
        logger.info("Test execute sql: OK!!! ---------------------------> TEST 18 OK!!!")

if __name__ == "__main__":
    unittest.main()