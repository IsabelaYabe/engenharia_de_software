import unittest
from unittest.mock import patch, MagicMock
import uuid
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), 'src')))
from relationships.product_review import ProductReview

class TestProductComplaint(unittest.TestCase):
    @patch("mysql.connector.connect") 
    def setUp(self, mock_connect):
        self.product_review = ProductReview(
            host="localhost",
            user="root",
            password="password",
            database="test_db"
        )
    @patch("relationships.product_review.ProductReview._create_table_")
    def test_create_table(self, mock_create_table):
        self.product_review._create_table()
        mock_create_table.assert_called_once()
    
    @patch("uuid.uuid4")
    @patch("relationships.product_review.ProductReview._insert_row")
    def test_insert_row(self, mock_insert_row, mock_uuid):  
        mock_uuid.return_value = uuid.UUID("12345678-1234-5678-1234-567812345678")
        result = self.product_review.insert_row("comment_id", "product_id", "user_id")

        mock_insert_row.assert_called_once_with(
            id="12345678-1234-5678-1234-567812345678",
            comment_id="comment_id",
            product_id="product_id",
            user_id="user_id"
            )
        self.assertEqual(result, "12345678-1234-5678-1234-567812345678")

    @patch("relationships.product_review.ProductReview.get_by_id")
    @patch("relationships.product_review.ProductReview._update_row")
    def test_update_row(self, mock_update_row, mock_get_by_id):
        comment_id = "12345678-1234-5678-1234-567812345678"

        self.product_review.update_row(comment_id, comment_id="new_comment_id", product_id ="new_product_id")
        mock_update_row.assert_called_once_with(comment_id, "id", comment_id="new_comment_id", product_id ="new_product_id")

    @patch("relationships.product_review.ProductReview._delete_row")
    def test_delete_row(self, mock_delete_row):
        comment_id = "12345678-1234-5678-1234-567812345678"
        self.product_review.delete_row(comment_id)
        mock_delete_row.assert_called_once_with(comment_id, "id")

    @patch("relationships.product_review.ProductReview._get_by_id")
    def test_get_by_id(self, mock_get_by_id):
        comment_id = "12345678-1234-5678-1234-567812345678"
        self.product_review.get_by_id(comment_id)

        mock_get_by_id.assert_called_once_with(comment_id, "id")

if __name__ == '__main__':
    unittest.main()