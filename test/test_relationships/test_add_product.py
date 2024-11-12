import unittest
from unittest.mock import patch, MagicMock
import uuid
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), 'src')))
from relationships.add_product import AddProduct

class TestAddProduct(unittest.TestCase):
    @patch("mysql.connector.connect") 
    def setUp(self, mock_connect):
        self.add_product = AddProduct(
            host="localhost",
            user="root",
            password="password",
            database="test_db"
        )
    @patch("relationships.add_product.AddProduct._create_table_")
    def test_create_table(self, mock_create_table):
        self.add_product._create_table()
        mock_create_table.assert_called_once()
    
    @patch("uuid.uuid4")
    @patch("relationships.add_product.AddProduct._insert_row")
    def test_insert_row(self, mock_insert_row, mock_uuid):  
        mock_uuid.return_value = uuid.UUID("12345678-1234-5678-1234-567812345678")
        result = self.add_product.insert_row("owner_id", "product_id", "vending_machine_id", 10)

        mock_insert_row.assert_called_once_with(
            id="12345678-1234-5678-1234-567812345678",
            owner_id="owner_id",
            product_id="product_id",
            vending_machine_id="vending_machine_id",
            quantity=10
        )
        self.assertEqual(result, "12345678-1234-5678-1234-567812345678")

    @patch("relationships.add_product.AddProduct.get_by_id")
    @patch("relationships.add_product.AddProduct._update_row")
    def test_update_row(self, mock_update_row, mock_get_by_id):
        add_id = "12345678-1234-5678-1234-567812345678"
    
        self.add_product.update_row(add_id, quantity=10)
        mock_update_row.assert_called_once_with(add_id, "id", quantity=10)

    @patch("relationships.add_product.AddProduct._delete_row")
    def test_delete_row(self, mock_delete_row):
        add_id = "12345678-1234-5678-1234-567812345678"
        self.add_product.delete_row(add_id)
        mock_delete_row.assert_called_once_with(add_id, "id")

    @patch("relationships.add_product.AddProduct._get_by_id")
    def test_get_by_id(self, mock_get_by_id):
        add_id = "12345678-1234-5678-1234-567812345678"
        self.add_product.get_by_id(add_id)

        mock_get_by_id.assert_called_once_with(add_id, "id")

if __name__ == '__main__':
    unittest.main()