"""
Module for Testing PurchaseProductSubUpdateStrategy Class.

This module provides a suite of unit tests for the `PurchaseProductSubUpdateStrategy` class using the `unittest` framework.
It validates the behavior of the update strategy for purchase-related operations, ensuring accurate stock adjustments 
and handling of edge cases.

Author: Isabela Yabe
Last Modified: 07/12/2024
Status: Complete

Dependencies:
    - unittest
    - unittest.mock
    - sub_strategy.sub_update_strategy.PurchaseProductSubUpdateStrategy
    - custom_logger.setup_logger
"""

import unittest
from unittest.mock import MagicMock, patch
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), 'src')))
from sub_strategy.sub_update_strategy import PurchaseProductSubUpdateStrategy
from custom_logger import setup_logger

logger = setup_logger()

class TestPurchaseProductSubUpdateStrategy(unittest.TestCase):
    """
    Test suite for the PurchaseProductSubUpdateStrategy class.

    This class tests the functionality of the `update` method, ensuring it correctly adjusts stock quantities, 
    handles cases of insufficient stock, and logs appropriate messages for failures or successful operations.
    """

    def setUp(self):
        """
        Set up the test environment before each test case.

        Creates an instance of PurchaseProductSubUpdateStrategy with mocked methods for `search_record` and `update_row`.
        """
        self.strategy = PurchaseProductSubUpdateStrategy()
        self.strategy.search_record = MagicMock()
        self.strategy.update_row = MagicMock()

    def test_update_success(self):
        """
        Test successful update of product stock.

        Verifies that when sufficient stock is available, the `update_row` method is called with the correct parameters.
        """
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
        """
        Test update with insufficient stock.

        Ensures that the `update_row` method is not called when the requested quantity exceeds the available stock.
        """
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
        """
        Test update with nonexistent product.

        Verifies that the `update_row` method is not called when the product is not found in the database.
        """
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
        """
        Test update failure.

        Ensures that an exception is raised when the `update_row` method fails to update the database.
        """
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