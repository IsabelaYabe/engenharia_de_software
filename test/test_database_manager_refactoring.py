import unittest
from unittest.mock import MagicMock, patch
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

    @patch("database_manager_refactoring.mysql.connector.connect")
    def test_modify_column_success(self, mock_connect):
        mock_connection = MagicMock()
        mock_connect.return_value = mock_connection
        mock_cursor = mock_connection.cursor.return_value

        expected_sql = "ALTER TABLE `test_table` RENAME COLUMN `col1` TO `col0`;"
        logger.debug(mock_cursor)
        print(mock_cursor)
        self.db_manager._modify_column("col1", "col0")

        mock_cursor.execute.assert_called_once_with(expected_sql)
        mock_connection.commit.assert_called_once()

if __name__ == "__main__":
    unittest.main()
    1906798800016