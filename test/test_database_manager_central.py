"""
    Module for unit testing the ProductProfile class.

    Author: Isabela Yabe 

    Dependencies: 
        - unittest
        - uuid
        - os
        - sys
        - DatabaseManagerCentral
        - ProductProfile
"""

import unittest
from unittest.mock import patch, MagicMock
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), 'src')))
from database_manager_central import DatabaseManagerCentral
from product_profile import ProductProfile


class TestDatabaseManagerCentral(unittest.TestCase):

    @patch("mysql.connector.connect")  # Mockando a conexão com MySQL
    def setUp(self, mock_connect):
        """
        This method sets up the environment for each test.
        Initializes a DatabaseManagerCentral instance and patches database connection.
        """
        mock_connection = MagicMock()
        mock_connect.return_value = mock_connection
        self.mock_cursor = mock_connection.cursor.return_value

        self.db_manager = DatabaseManagerCentral("localhost", "root", "password", "test_db")

    @patch("mysql.connector.connect")
    def test_create_all_tables(self, mock_connect):
        """
        Test if _create_all_tables correctly calls the create_table method.
        """
        self.db_manager.product_manager.create_table = MagicMock()

        self.db_manager._create_all_tables()

        self.db_manager.product_manager.create_table.assert_called_once()

    @patch("mysql.connector.connect")
    def test_drop_all_tables(self, mock_connect):
        """
        Test if _drop_all_tables correctly calls the delete_table method.
        """
        self.db_manager.product_manager.delete_table = MagicMock()

        self.db_manager._drop_all_tables()

        self.db_manager.product_manager.delete_table.assert_called_once()

    @patch("mysql.connector.connect")
    def test_reset_database(self, mock_connect):
        """
        Test if _reset_database calls both _drop_all_tables and _create_all_tables.
        """
        self.db_manager._drop_all_tables = MagicMock()
        self.db_manager._create_all_tables = MagicMock()

        self.db_manager._reset_database()

        self.db_manager._drop_all_tables.assert_called_once()
        self.db_manager._create_all_tables.assert_called_once()

    @patch("mysql.connector.connect")
    def test_add_instance(self, mock_connect):
        """
        Test if _add_instance correctly adds an instance using the product manager.
        """
        self.db_manager.product_manager.create_product = MagicMock(return_value="product_id_123")

        instance_data = {
            "name": "Test Product",
            "description": "A test description",
            "price": 19.99,
            "quantity": 10
        }

        result = self.db_manager._add_instance(self.db_manager.product_manager, **instance_data)

        self.db_manager.product_manager.create_product.assert_called_once_with(
            name="Test Product",
            description="A test description",
            price=19.99,
            quantity=10
        )
        
        self.assertTrue(result)

    @patch("mysql.connector.connect")
    def test_add_instance_with_invalid_manager(self, mock_connect):
        """
        Test if _add_instance handles an invalid manager gracefully.
        """
        class FakeManager:
            table_name = "unknowns"
        
        fake_manager = FakeManager()

        result = self.db_manager._add_instance(fake_manager, name="Invalid Test")

        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()
