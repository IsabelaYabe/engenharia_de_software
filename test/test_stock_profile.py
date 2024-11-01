import unittest
from unittest.mock import patch, MagicMock
import sys
import os
sys.path.append(os.path.abspath('src/profiles'))
from stock_profile import StockProfile

class TestStockProfile(unittest.TestCase):
    
    @patch('mysql.connector.connect')
    def setUp(self, mock_connect):
        """Set up the mock connection and cursor for the StockProfile tests."""
        self.mock_connection = MagicMock()
        self.mock_cursor = MagicMock()
        self.mock_connection.cursor.return_value = self.mock_cursor
        mock_connect.return_value = self.mock_connection
        
        self.db_config = {
            "host": "localhost",
            "user": "root",
            "password": "Alacazumba123*",
            "database": "test_database"
        }
        self.stock_profile = StockProfile(**self.db_config)
    
    def test_get_stock_info(self):
        """Test the get_stock_info method to ensure it returns correct stock data."""
        # Simulate the data returned by the cursor
        self.mock_cursor.fetchall.return_value = [
            (1, "Product A", 10.99, 100, 1, "Machine A"),
            (2, "Product B", 12.50, 200, 2, "Machine B"),
        ]
        
        expected_result = [
            {
                'product_id': 1,
                'product_name': "Product A",
                'product_price': 10.99,
                'product_quantity': 100,
                'vending_machine_id': 1,
                'vending_machine_name': "Machine A"
            },
            {
                'product_id': 2,
                'product_name': "Product B",
                'product_price': 12.50,
                'product_quantity': 200,
                'vending_machine_id': 2,
                'vending_machine_name': "Machine B"
            }
        ]
        
        result = self.stock_profile.get_stock_info()
        self.assertEqual(result, expected_result)
        
        # Ensure the correct SQL query was executed
        self.mock_cursor.execute.assert_called_once_with("""
        SELECT 
            p.ProductID AS product_id, 
            p.Name AS product_name, 
            p.Price AS product_price,
            p.Quantity AS product_quantity,
            p.VMID AS vending_machine_id,
            vm.Name AS vending_machine_name
        FROM 
            Products AS p
        JOIN 
            VMs AS vm ON p.VMID = vm.VMID
        """)
    
    def test_close(self):
        """Test if the close method closes the cursor and the connection."""
        self.stock_profile.close()
        
        # Ensure the cursor and connection close methods are called
        self.mock_cursor.close.assert_called_once()
        self.mock_connection.close.assert_called_once()
    
    def tearDown(self):
        """Clean up after tests."""
        self.stock_profile.close()

if __name__ == '__main__':
    unittest.main()
