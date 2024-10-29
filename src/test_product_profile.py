"""
    Module for unit testing the ProductProfile class.

    Author: Isabela Yabe 

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
import uuid
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), 'src')))
from product_profile import ProductProfile


class TestProductProfile(unittest.TestCase):

    @patch("mysql.connector.connect")  # Mockando a conexão ao MySQL
    def setUp(self, mock_connect):
        """
        This method sets up the environment for each test.
        Initializes a ProductProfile instance and patches database connection.
        """
        mock_connection = MagicMock()
        mock_connect.return_value = mock_connection
        self.mock_cursor = mock_connection.cursor.return_value

        self.product_profile = ProductProfile("localhost", "root", "password", "test_db")
        self.product_id = str(uuid.uuid4())

    @patch("mysql.connector.connect")
    def test_create_product(self, mock_connect):
        """
        Test if the create_product method inserts a new product into the database correctly.
        """
        mock_connection = MagicMock()
        mock_connect.return_value = mock_connection
        mock_cursor = mock_connection.cursor.return_value

        product_id = self.product_profile.create_product("Test Product", "A test description", 19.99, 10)

        expected_sql = "INSERT INTO products (product_id, name, description, price, quantity) VALUES (%s, %s, %s, %s, %s);"

        mock_cursor.execute.assert_called_with(expected_sql, (product_id, "Test Product", "A test description", 19.99, 10))

        mock_connection.commit.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_connection.close.assert_called_once()
    
    @patch("mysql.connector.connect")
    def test_get_product(self, mock_connect):
        """
        Test if the get_product method retrieves a product by its ID and returns all product details.
        """
        mock_connection = MagicMock()
        mock_connect.return_value = mock_connection
        mock_cursor = mock_connection.cursor.return_value

        mock_cursor.fetchone.return_value = (
            self.product_id, "Test Product", "A test description", 19.99, 100
        )

        product = self.product_profile.get_product(self.product_id)

        expected_product = {
            "product_id": self.product_id,
            "name": "Test Product",
            "description": "A test description",
            "price": 19.99,
            "quantity": 100
        }

        self.assertEqual(product, expected_product)

        mock_cursor.execute.assert_called_with(
            "SELECT id, name, description, price, quantity FROM products WHERE id = %s", 
            (self.product_id,)
        )

        mock_cursor.close.assert_called_once()
        mock_connection.close.assert_called_once()
    
    @patch("mysql.connector.connect")
    def test_update_price(self, mock_connect):
        """
        Test if the update_price method updates the product's price in the database.
        """
        mock_connection = MagicMock()
        mock_connect.return_value = mock_connection
        mock_cursor = mock_connection.cursor.return_value

        self.product_profile.update_price(self.product_id, 25.99)

        expected_sql = f"UPDATE products SET price = %s WHERE product_id = '{self.product_id}';"

        mock_cursor.execute.assert_called_with(expected_sql, (25.99,))
    
        mock_connection.commit.assert_called_once()
        mock_cursor.close.assert_called_once()
    
    @patch("mysql.connector.connect")
    def test_update_name(self, mock_connect):
        """
        Test if the update_name method updates the product's name in the database.
        """
        mock_connection = MagicMock()
        mock_connect.return_value = mock_connection
        mock_cursor = mock_connection.cursor.return_value

        self.product_profile.update_name(self.product_id, "Updated Product")

        expected_sql = f"UPDATE products SET name = %s WHERE product_id = '{self.product_id}';"
        mock_cursor.execute.assert_called_with(expected_sql, ("Updated Product",))
        mock_connection.commit.assert_called_once()
        mock_cursor.close.assert_called_once()
    
    @patch("mysql.connector.connect")
    def test_delete_product(self, mock_connect):
        """
        Test if the delete_product method removes a product from the database.
        """
        mock_connection = MagicMock()
        mock_connect.return_value = mock_connection
        mock_cursor = mock_connection.cursor.return_value

        self.product_profile.delete_product(self.product_id)

        expected_sql = "DELETE FROM products WHERE id = %s;"
        mock_cursor.execute.assert_called_with(expected_sql, (self.product_id,))
        mock_connection.commit.assert_called_once()
        mock_cursor.close.assert_called_once()
    

if __name__ == '__main__':
    unittest.main()