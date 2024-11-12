import unittest
from unittest.mock import MagicMock, patch
from flask import Flask, jsonify, request
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), 'src')))
from transaction_validation_strategy.foreign_key_exists_strategy import ForeignKeyExistsStrategy
from transaction_validation_strategy.check_purchase_quantity_strategy import CheckPurchaseQuantityStrategy
from decorators import transaction_validations

# Mocked central database manager
class MockDatabaseManagerCentral:
    def __init__(self):
        self.tables = {
            "users": MagicMock(),
            "products": MagicMock(),
            "vending_machines": MagicMock()
        }

    def get_table(self, table_name):
        return self.tables.get(table_name, None)

class TestTransactionValidationsDecorator(unittest.TestCase):
    def setUp(self):
        self.mock_db_central = MockDatabaseManagerCentral()

        self.app = Flask(__name__)
        self.app.testing = True
        self.client = self.app.test_client()

        self.foreign_key_strategy = ForeignKeyExistsStrategy()
        self.quantity_strategy = CheckPurchaseQuantityStrategy()

        patcher = patch("main_file.database_manager_central", self.mock_db_central)
        self.addCleanup(patcher.stop)
        patcher.start()

    @transaction_validations([ForeignKeyExistsStrategy(), CheckPurchaseQuantityStrategy()])
    def insert_row_with_validation(self, user_id, product_id, vending_machine_id, quantity, amount_paid_per_unit):

        return jsonify({"message": "Transaction inserted successfully"}), 201

    def test_insert_row_foreign_key_exists(self):
        self.mock_db_central.tables["users"].get_by_id.return_value = {"id": "user_id"}
        self.mock_db_central.tables["products"].get_by_id.return_value = {"id": "product_id", "quantity": 10}
        self.mock_db_central.tables["vending_machines"].get_by_id.return_value = {"id": "vending_machine_id"}

        with self.app.test_request_context():
            response = self.insert_row_with_validation("user_id", "product_id", "vending_machine_id", 5, 2.50)
            self.assertEqual(response[1], 201)
            self.assertEqual(response[0].json, {"message": "Transaction inserted successfully"})

'''    def test_insert_row_foreign_key_does_not_exist(self):
        self.mock_db_central.tables["users"].get_by_id.return_value = None  
        self.mock_db_central.tables["products"].get_by_id.return_value = {"id": "product_id", "quantity": 10}
        self.mock_db_central.tables["vending_machines"].get_by_id.return_value = {"id": "vending_machine_id"}

        with self.app.test_request_context():
            response = self.insert_row_with_validation("user_id", "product_id", "vending_machine_id", 5, 2.50)
            self.assertEqual(response[1], 400)
            self.assertIn("does not exist", response[0].json["error"])

    def test_insert_row_insufficient_quantity(self):
        self.mock_db_central.tables["users"].get_by_id.return_value = {"id": "user_id"}
        self.mock_db_central.tables["products"].get_by_id.return_value = {"id": "product_id", "quantity": 3}
        self.mock_db_central.tables["vending_machines"].get_by_id.return_value = {"id": "vending_machine_id"}

        with self.app.test_request_context():
            response = self.insert_row_with_validation("user_id", "product_id", "vending_machine_id", 5, 2.50)
            self.assertEqual(response[1], 400)
            self.assertIn("Insufficient quantity available", response[0].json["error"])

    def test_insert_row_sufficient_quantity(self):
        self.mock_db_central.tables["users"].get_by_id.return_value = {"id": "user_id"}
        self.mock_db_central.tables["products"].get_by_id.return_value = {"id": "product_id", "quantity": 10}
        self.mock_db_central.tables["vending_machines"].get_by_id.return_value = {"id": "vending_machine_id"}

        with self.app.test_request_context():
            response = self.insert_row_with_validation("user_id", "product_id", "vending_machine_id", 5, 2.50)
            self.assertEqual(response[1], 201)
            self.assertEqual(response[0].json, {"message": "Transaction inserted successfully"})'''

if __name__ == "__main__":
    unittest.main()
