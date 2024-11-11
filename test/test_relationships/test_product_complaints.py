import unittest
from unittest.mock import patch, MagicMock
import uuid
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), 'src')))
from relationships.product_complaint import ProductComplaint

class TestProductComplaint(unittest.TestCase):
    @patch("mysql.connector.connect") 
    def setUp(self, mock_connect):
        self.product_complaints = ProductComplaint(
            host="localhost",
            user="root",
            password="password",
            database="test_db"
        )
    @patch("relationships.product_complaint.ProductComplaint._create_table_")
    def test_create_table(self, mock_create_table):
        self.product_complaints._create_table()
        mock_create_table.assert_called_once()
    
    @patch("uuid.uuid4")
    @patch("relationships.product_complaint.ProductComplaint._insert_row")
    def test_insert_row(self, mock_insert_row, mock_uuid):  
        mock_uuid.return_value = uuid.UUID("12345678-1234-5678-1234-567812345678")
        result = self.product_complaints.insert_row("complaint_id", "product_id", "user_id")

        mock_insert_row.assert_called_once_with(
            id="12345678-1234-5678-1234-567812345678",
            complaint_id="complaint_id",
            product_id="product_id",
            user_id="user_id"
            )
        self.assertEqual(result, "12345678-1234-5678-1234-567812345678")

    @patch("relationships.product_complaint.ProductComplaint.get_by_id")
    @patch("relationships.product_complaint.ProductComplaint._update_row")
    def test_update_row(self, mock_update_row, mock_get_by_id):
        complaint_id = "12345678-1234-5678-1234-567812345678"

        self.product_complaints.update_row(complaint_id, complaint_id="new_complaint_id", product_id ="new_product_id")
        mock_update_row.assert_called_once_with(complaint_id, "id", complaint_id="new_complaint_id", product_id ="new_product_id")

    @patch("relationships.product_complaint.ProductComplaint._delete_row")
    def test_delete_row(self, mock_delete_row):
        complaint_id = "12345678-1234-5678-1234-567812345678"
        self.product_complaints.delete_row(complaint_id)
        mock_delete_row.assert_called_once_with(complaint_id, "id")

    @patch("relationships.product_complaint.ProductComplaint._get_by_id")
    def test_get_by_id(self, mock_get_by_id):
        complaint_id = "12345678-1234-5678-1234-567812345678"
        self.product_complaints.get_by_id(complaint_id)

        mock_get_by_id.assert_called_once_with(complaint_id, "id")

if __name__ == '__main__':
    unittest.main()