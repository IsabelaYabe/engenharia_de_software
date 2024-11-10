"""
    Module for unit testing the ProductProfile class.

    This module provides unit tests for the `ProductProfile` class, which is responsible for managing
    CRUD operations on a product profile database table.

    Author: Isabela Yabe
    Last Modified: 09/11/2024
    Status: Complete

    Dependencies:
        - unittest
        - unittest.mock
        - uuid
        - os
        - sys
        - ProductProfile
        - mysql.connector
"""

import unittest
from unittest.mock import patch, MagicMock
import uuid
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), 'src')))
from product_profile import ProductProfile


class TestProductProfile(unittest.TestCase):
    """
    TestProductProfile class.

    This class contains unit tests for the `ProductProfile` class, verifying that the CRUD methods
    function as expected in handling product profile data.

    Methods:
        - setUp: Initializes a ProductProfile instance for testing.
        - test_create_table: Tests table creation to ensure it is called correctly.
        - test_insert_row: Tests inserting a new product, checking that the row insertion occurs as expected.
        - test_update_row: Tests updating an existing product and verifies the updated data.
        - test_delete_row: Tests the deletion of a product by ID.
        - test_get_by_id: Tests retrieving a product by its ID and checks if the returned data is correct.
    """
    @patch("mysql.connector.connect") 
    def setUp(self, mock_connect):
        """
        Sets up a ProductProfile instance for testing by mocking the MySQL connection.
        
        Args:
            mock_connect: Mock object to simulate the MySQL connection.
        """
        self.product_profile = ProductProfile(
            host = "localhost",
            user = "root",
            password = "password",
            database="test_db"
        )

    @patch("product_profile.ProductProfile._create_table_")
    def test_create_table(self, mock_create_table):
        """
        Tests that the _create_table method correctly triggers the table creation.
        
        Args:
            mock_create_table: Mock object to simulate the table creation.
        """
        self.product_profile._create_table()
        mock_create_table.assert_called_once()
    
    @patch("uuid.uuid4")
    @patch("product_profile.ProductProfile._insert_row")
    def test_insert_row(self, mock_insert_row, mock_uuid):  
        """
        Tests inserting a new product into the `products` table.

        Args:
            mock_insert_row: Mock object to simulate row insertion.
            mock_uuid: Mock object to generate a consistent UUID for testing.
        """  
        mock_uuid.return_value = uuid.UUID("12345678-1234-5678-1234-567812345678")

        result = self.product_profile.insert_row("Test Product", "Description", 1.99, 10)
        mock_insert_row.assert_called_once_with(
            id="12345678-1234-5678-1234-567812345678",
            name="Test Product",
            description="Description",
            price=1.99,
            quantity=10
        )
        self.assertEqual(result, "12345678-1234-5678-1234-567812345678")
 
    @patch("product_profile.ProductProfile.get_by_id")
    @patch("product_profile.ProductProfile._update_row")
    def test_update_row(self, mock_update_row, mock_get_by_id):
        """
        Tests updating an existing product's details.

        Args:
            mock_update_row: Mock object to simulate row updating.
            mock_get_by_id: Mock object to retrieve product details.
        """
        product_id = "12345678-1234-5678-1234-567812345678"

        self.product_profile.update_row(product_id, name="new name", price=2.99)

        mock_update_row.assert_called_once_with(product_id, "id", name="new name", price=2.99)

    @patch("product_profile.ProductProfile._delete_row")
    def test_delete_row(self, mock_delete_row):
        """
        Tests deleting a product by ID.

        Args:
            mock_delete_row: Mock object to simulate row deletion.
        """
        product_id = str(uuid.uuid4())
        self.product_profile.delete_row(product_id)

        mock_delete_row.assert_called_once_with(product_id, "id")

    @patch("product_profile.ProductProfile._get_by_id")
    def test_get_by_id(self, mock_get_by_id):
        """
        Tests retrieving a product by its ID.

        Args:
            mock_get_by_id: Mock object to simulate retrieval of a product by ID.
        """
        product_id = str(uuid.uuid4())
        mock_get_by_id.return_value = (product_id, "name", "description", 1.99, 10)

        result = self.product_profile.get_by_id(product_id)
        expected_result = {
            "id": product_id, 
            "name": "name",
            "description": "description",
            "price": 1.99,
            "quantity": 10
            }

        mock_get_by_id.assert_called_once_with(product_id, "id")
        self.assertEqual(result, expected_result)
        
if __name__ == '__main__':
    unittest.main()