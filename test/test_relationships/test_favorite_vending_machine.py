import unittest
from unittest.mock import patch, MagicMock
import uuid
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), 'src')))
from relationships.favorite_vending_machine import FavoriteVM

class TestFavoriteVM(unittest.TestCase):
    @patch("mysql.connector.connect") 
    def setUp(self, mock_connect):
        self.favorite_vending_machine = FavoriteVM(
            host="localhost",
            user="root",
            password="password",
            database="test_db"
        )
        
    @patch("relationships.favorite_vending_machine.FavoriteVM._create_table_")
    def test_create_table(self, mock_create_table):
        self.favorite_vending_machine._create_table()
        mock_create_table.assert_called_once()
    
    @patch("uuid.uuid4")
    @patch("relationships.favorite_vending_machine.FavoriteVM._insert_row")
    def test_insert_row(self, mock_insert_row, mock_uuid):  
        mock_uuid.return_value = uuid.UUID("12345678-1234-5678-1234-567812345678")
        result = self.favorite_vending_machine.insert_row("user_id", "vending_machine_id")

        mock_insert_row.assert_called_once_with(
            id="12345678-1234-5678-1234-567812345678",
            user_id="user_id",
            vending_machine_id="vending_machine_id"
        )
        self.assertEqual(result, "12345678-1234-5678-1234-567812345678")

    @patch("relationships.favorite_vending_machine.FavoriteVM.get_by_id")
    @patch("relationships.favorite_vending_machine.FavoriteVM._update_row")
    def test_update_row(self, mock_update_row, mock_get_by_id):
        favorite_id = "12345678-1234-5678-1234-567812345678"
    
        self.favorite_vending_machine.update_row(favorite_id, user_id="new owner")
        mock_update_row.assert_called_once_with(favorite_id, "id", user_id="new owner")

    @patch("relationships.favorite_vending_machine.FavoriteVM._delete_row")
    def test_delete_row(self, mock_delete_row):
        favorite_id = "12345678-1234-5678-1234-567812345678"
        self.favorite_vending_machine.delete_row(favorite_id)
        mock_delete_row.assert_called_once_with(favorite_id, "id")

    @patch("relationships.favorite_vending_machine.FavoriteVM._get_by_id")
    def test_get_by_id(self, mock_get_by_id):
        favorite_id = "12345678-1234-5678-1234-567812345678"
        self.favorite_vending_machine.get_by_id(favorite_id)

        mock_get_by_id.assert_called_once_with(favorite_id, "id")

if __name__ == '__main__':
    unittest.main()