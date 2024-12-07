import unittest
from unittest.mock import MagicMock, patch
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), 'src')))
from sub_strategy.sub_update_strategy import PurchaseProductSubUpdateStrategy
from custom_logger import setup_logger

logger = setup_logger()


class TestPurchaseProductSubUpdateStrategy(unittest.TestCase):
    def setUp(self):
        self.strategy = PurchaseProductSubUpdateStrategy()
        self.strategy.search_record = MagicMock()
        self.strategy.update_row = MagicMock()

    def test_update_success(self):
        data = {
            "name": "Test Product",
            "vending_machine_id": 1,
            "quantity": 5,
        }
        mock_existing_product = {"id": 1, "name": "Test Product", "quantity": 10}
        self.strategy.search_record.return_value = [mock_existing_product]

        self.strategy.update(data)

        self.strategy.search_record.assert_called_once_with(
            name="Test Product", vending_machine_id=1
        )
        self.strategy.update_row.assert_called_once_with(1, quantity=5)
        logger.debug("Test update success passed: OK!!! ---------------------------> TEST 1 OK!!!")

    def test_update_insufficient_stock(self):
        data = {
            "name": "Test Product",
            "vending_machine_id": 1,
            "quantity": 15,
        }
        mock_existing_product = {"id": 1, "name": "Test Product", "quantity": 10}
        self.strategy.search_record.return_value = [mock_existing_product]

        self.strategy.update(data)

        self.strategy.search_record.assert_called_once_with(
            name="Test Product", vending_machine_id=1
        )
        self.strategy.update_row.assert_not_called()
        logger.debug("Test update insufficient stock passed: OK!!! ---------------------------> TEST 2 OK!!!")

    def test_update_product_not_found(self):
        data = {
            "name": "Nonexistent Product",
            "vending_machine_id": 1,
            "quantity": 5,
        }
        self.strategy.search_record.return_value = []

        self.strategy.update(data)

        self.strategy.search_record.assert_called_once_with(
            name="Nonexistent Product", vending_machine_id=1
        )
        self.strategy.update_row.assert_not_called()
        logger.debug("Test update product not found passed: OK!!! ---------------------------> TEST 3 OK!!!")

    def test_update_failure(self):
        data = {
            "name": "Test Product",
            "vending_machine_id": 1,
            "quantity": 5,
        }
        mock_existing_product = {"id": 1, "name": "Test Product", "quantity": 10}
        self.strategy.search_record.return_value = [mock_existing_product]
        self.strategy.update_row.side_effect = Exception("Database error")

        with self.assertRaises(Exception):
            self.strategy.update(data)

        self.strategy.search_record.assert_called_once_with(
            name="Test Product", vending_machine_id=1
        )
        self.strategy.update_row.assert_called_once_with(1, quantity=5)
        logger.debug("Test update failure passed: OK!!! ---------------------------> TEST 4 OK!!!")


if __name__ == "__main__":
    unittest.main()