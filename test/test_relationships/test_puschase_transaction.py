import unittest
from unittest.mock import patch, MagicMock
import uuid
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), 'src')))
from relationships.purchase_transaction import PurchaseTransaction

class TestPurchaseTransaction(unittest.TestCase):
    @patch("mysql.connector.connect") 
    def setUp(self, mock_connect):
        self.purchase_transaction = PurchaseTransaction(
            host="localhost",
            user="root",
            password="password",
            database="test_db"
        )
    @patch("relationships.purchase_transaction.PurchaseTransaction._create_table_")
    def test_create_table(self, mock_create_table):
        self.purchase_transaction._create_table()
        mock_create_table.assert_called_once()
    
    @patch("uuid.uuid4")
    @patch("relationships.purchase_transaction.PurchaseTransaction._insert_row")
    def test_insert_row(self, mock_insert_row, mock_uuid):  
        mock_uuid.return_value = uuid.UUID("12345678-1234-5678-1234-567812345678")
        result = self.purchase_transaction.insert_row("user_id", "product_id", "vending_machine_id", 5, 9.99)

        mock_insert_row.assert_called_once_with(
            id="12345678-1234-5678-1234-567812345678",
            user_id="user_id",
            product_id="product_id",
            vending_machine_id="vending_machine_id",
            quantity=5,
            amount_paid_per_unit=9.99
        )
        self.assertEqual(result, "12345678-1234-5678-1234-567812345678")

    @patch("relationships.purchase_transaction.PurchaseTransaction.get_by_id")
    @patch("relationships.purchase_transaction.PurchaseTransaction._update_row")
    def test_update_row(self, mock_update_row, mock_get_by_id):
        transaction_id = "12345678-1234-5678-1234-567812345678"
    
        self.purchase_transaction.update_row(transaction_id, quantity=10, amount_paid_per_unit=8.99)
        mock_update_row.assert_called_once_with(transaction_id, "id", quantity=10, amount_paid_per_unit=8.99)

    @patch("relationships.purchase_transaction.PurchaseTransaction._delete_row")
    def test_delete_row(self, mock_delete_row):
        transaction_id = "12345678-1234-5678-1234-567812345678"
        self.purchase_transaction.delete_row(transaction_id)
        mock_delete_row.assert_called_once_with(transaction_id, "id")

    @patch("relationships.purchase_transaction.PurchaseTransaction._get_by_id")
    def test_get_by_id(self, mock_get_by_id):
        transaction_id = "12345678-1234-5678-1234-567812345678"
        self.purchase_transaction.get_by_id(transaction_id)

        mock_get_by_id.assert_called_once_with(transaction_id, "id")

if __name__ == '__main__':
    unittest.main()