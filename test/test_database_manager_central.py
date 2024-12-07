"""
Module for Testing DatabaseManagerCentral Class.

This module provides a suite of unit tests for the `DatabaseManagerCentral` class using the `unittest` framework.
It tests various operations such as table management, CRUD operations, and proper instantiation of dependent classes.

Author: Isabela Yabe
Last Modified: 19/11/2024
Status: Complete

Dependencies:
    - unittest
    - unittest.mock
    - custom_logger.setup_logger
    - database_manager_central.DatabaseManagerCentral
"""

import unittest
from unittest.mock import MagicMock, patch
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.getcwd(),'src')))
from database_manager_central import DatabaseManager, DatabaseManagerCentral, Config, ConfigPub, ConfigSub
from event_manager.event_manager import EventManager
from sub_strategy.sub_update_strategy import PurchaseProductSubUpdateStrategy
from custom_logger import setup_logger

logger = setup_logger()

class TestDatabaseManagerCentral(unittest.TestCase):
    """
    TestDatabaseManagerCentral class.

    This class provides unit tests for the `DatabaseManagerCentral` class, focusing on its ability to manage 
    multiple table managers, perform initializations, and handle edge cases.
    """

    
    def setUp(self):
        """
        Set up the test environment before each test case.
        """
        self.host = "localhost"
        self.user = "test_user"
        self.password = "test_password"
        self.database = "test_database"

        self.mock_event_manager = MagicMock(spec=EventManager)
        self.mock_event_manager.update_strategies = {"PurchaseProductEvent": MagicMock(spec=PurchaseProductSubUpdateStrategy)}

        def create_config(table_name, columns, pub=None, sub=None):
            return Config(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                table_name=table_name,
                columns=columns,
            ), pub, sub
        
        self.products_config, self.products_config_pub, self.products_config_sub = create_config(
            "products_profile",
            ["id", "name", "description", "price", "quantity", "vending_machine_id", "timestamp"],
            sub=ConfigSub(event_manager=self.mock_event_manager, events_type_sub=["PurchaseProductEvent"])
        )

        self.users_config, self.users_config_pub, self.users_config_sub = create_config(
            "users_profile",
            ["id", "username", "email", "password", "first_name", "last_name", "birthdate", "phone number", "address", "budget"]
        )

        self.vending_machines_config, self.vending_machines_config_pub, self.vending_machines_config_sub = create_config(
            "vending_machines_profile",
            ["id", "name", "location", "status", "timestamp", "owner_id"]
        )

        self.owners_config, self.owners_config_pub, self.owners_config_sub = create_config(
            "owners_profile",
            ["id", "ownername", "email", "password", "first_name", "last_name", "birthdate", "phone_number", "address", "budget"]
        )

        self.purchase_transaction_config, self.purchase_transaction_config_pub, self.purchase_transaction_config_sub = create_config(
            "purchase_transaction",
            ["id", "user_id", "product_id", "vending_machine_id", "timestamp", "quantity", "amount_paid_per_unit"],
            pub=ConfigPub(event_manager=self.mock_event_manager, events_type_pub=["PurchaseProductEvent"])
        )
    
    def test_products_profile_initialization(self):
        """
        Test initialization of the products_profile table.
        """
        db_manager_central = DatabaseManagerCentral(
            host=self.host, user=self.user, password=self.password, database=self.database
        )
        products_table = db_manager_central.products_profile

        self.assertEqual(products_table.table_name, "products_profile")
        self.assertListEqual(
            products_table.columns,
            ["id", "name", "description", "price", "quantity", "vending_machine_id", "timestamp"],
        )
        self.assertIsNone(self.products_config_pub)
        self.assertEqual(
            self.products_config_sub.event_manager.update_strategies["PurchaseProductEvent"],
            self.mock_event_manager.update_strategies["PurchaseProductEvent"]
        )
        logger.info("Test connect: OK!!! ---------------------------> TEST 1 OK!!!")

    def test_insert_record_no_foreign_keys(self):
        """
        Test insert_record without foreign keys.
        """
        db_manager_central = DatabaseManagerCentral(
            host=self.host, user=self.user, password=self.password, database=self.database
        )

        with patch.object(db_manager_central.products_profile, 'insert_row', return_value="new_product_id") as mock_insert_row:
            data = {"name": "Test Product", "description": "A test product", "price": 10.0, "quantity": 100}
            record_id = db_manager_central.insert_record("products_profile", data)

            mock_insert_row.assert_called_once_with(**data)

            self.assertEqual(record_id, "new_product_id")
            logger.info("Test insert_record_no_foreign_keys: OK!!! ---------------------------> TEST 2 OK!!!")

    def test_insert_record_with_valid_foreign_keys(self):
        """
        Test insert_record with valid foreign keys.
        """
        db_manager_central = DatabaseManagerCentral(
            host=self.host, user=self.user, password=self.password, database=self.database
        )

        with patch.object(db_manager_central.vending_machines_profile, 'search_record', return_value=True) as mock_search_record, \
             patch.object(db_manager_central.products_profile, 'insert_row', return_value="new_product_id") as mock_insert_row:

            data = {"name": "Test Product", "description": "A test product", "price": 10.0, "quantity": 100, "vending_machine_id": "valid_id"}
            foreign_keys = {"vending_machines_profile": "vending_machine_id"}
            record_id = db_manager_central.insert_record("products_profile", data, foreign_keys)

            mock_search_record.assert_called_once_with(vending_machine_id="valid_id")

            mock_insert_row.assert_called_once_with(**data)

            self.assertEqual(record_id, "new_product_id")
            logger.info("Test insert_record_with_valid_foreign_keys: OK!!! ---------------------------> TEST 3 OK!!!")

    def test_insert_record_with_invalid_foreign_key(self):
        """
        Test insert_record with an invalid foreign key.
        """
        db_manager_central = DatabaseManagerCentral(
            host=self.host, user=self.user, password=self.password, database=self.database
        )

        with patch.object(db_manager_central.vending_machines_profile, 'search_record', return_value=False) as mock_search_record:
            data = {"name": "Test Product", "description": "A test product", "price": 10.0, "quantity": 100, "vending_machine_id": "invalid_id"}
            foreign_keys = {"vending_machines_profile": "vending_machine_id"}

            with self.assertRaises(ValueError) as context:
                db_manager_central.insert_record("products_profile", data, foreign_keys)

            mock_search_record.assert_called_once_with(vending_machine_id="invalid_id")

            self.assertEqual(str(context.exception), "Foreign key value 'invalid_id' does not exist in table 'vending_machines_profile'.")
            logger.info("Test insert_record_with_invalid_foreign_key: OK!!! ---------------------------> TEST 4 OK!!!")

    def test_insert_record_table_not_found(self):
        """
        Test insert_record with a non-existent table.
        """
        db_manager_central = DatabaseManagerCentral(
            host=self.host, user=self.user, password=self.password, database=self.database
        )

        data = {"name": "Test Product", "description": "A test product", "price": 10.0, "quantity": 100}

        with self.assertRaises(ValueError) as context:
            db_manager_central.insert_record("non_existent_table", data)

        self.assertEqual(str(context.exception), "Table 'non_existent_table' not found in instance tables.")
        logger.info("Test insert_record_table_not_found: OK!!! ---------------------------> TEST 5 OK!!!")  

    def test_add_user(self):
        """
        Test adding a new user to the database.
        """
        logger.debug("Starting test_add_user ---------------------------> TEST 6")
        db_manager_central = DatabaseManagerCentral(
            host=self.host, user=self.user, password=self.password, database=self.database
        )

        user_data = {
            "username": "test_user",
            "email": "test_user@example.com",
            "password": "secure_password",
            "first_name": "Test",
            "last_name": "User",
            "birthdate": "1990-01-01",
            "phone_number": "1234567890",
            "address": "123 Test Street",
            "budget": 100.0,
        }

        with patch.object(db_manager_central.users_profile, 'search_record', return_value=True) as mock_search_record, \
             patch.object(db_manager_central.users_profile, 'insert_row', return_value="new_user_id") as mock_insert_row:

            user_id = db_manager_central.add_user(**user_data)

            mock_insert_row.assert_called_once_with(**user_data)

            mock_search_record.assert_not_called()

            self.assertEqual(user_id, "new_user_id")
            logger.info("Test add_user: OK!!! ---------------------------> TEST 6 OK!!!")

    def test_add_purchase_transaction_success(self):
        """
        Test successful addition of a purchase transaction.
        """
        logger.debug("Starting test_add_purchase_transaction_success ---------------------------> TEST 7")
        db_manager_central = DatabaseManagerCentral(
            host=self.host, user=self.user, password=self.password, database=self.database
        )

        with patch.object(db_manager_central.instance_tables.purchase_transaction, "insert_row", return_value="transaction_id") as mock_insert_row, \
             patch.object(db_manager_central.instance_tables.users_profile, "search_record", return_value=True) as mock_user_search, \
             patch.object(db_manager_central.instance_tables.products_profile, "search_record", return_value=[{"id": "valid_product", "quantity": 10}]) as mock_product_search, \
             patch.object(db_manager_central.instance_tables.vending_machines_profile, "search_record", return_value=True) as mock_vm_search, \
             patch.object(db_manager_central._DatabaseManagerCentral__purchase_transaction_config_pub.event_manager, "notify") as mock_notify:

            user_id = "valid_user"
            product_id = "valid_product"
            vending_machine_id = "valid_vm"
            quantity = 2
            amount_paid_per_unit = 10.0

            transaction_id = db_manager_central.add_purchase_transaction(
                user_id, product_id, vending_machine_id, quantity, amount_paid_per_unit
            )

            mock_user_search.assert_called_with(user_id="valid_user")
            mock_product_search.assert_called_with(product_id="valid_product")
            mock_vm_search.assert_called_once_with(vending_machine_id="valid_vm")

            mock_insert_row.assert_called_once_with(
                user_id="valid_user", product_id="valid_product", vending_machine_id="valid_vm",
                quantity=2, amount_paid_per_unit=10.0
            )

            event_data = {
                "transaction_id": "transaction_id",
                "user_id": "valid_user",
                "product_id": "valid_product",
                "vending_machine_id": "valid_vm",
                "quantity": 2,
                "amount_paid_per_unit": 10.0,
            }
            mock_notify.assert_called_once_with("PurchaseProductEvent", event_data)

            self.assertEqual(transaction_id, "transaction_id")
            logger.info("Test add_purchase_transaction_success: OK!!! ---------------------------> TEST 7 OK!!!")


    def test_add_purchase_transaction_invalid_foreign_key(self):
        """
        Test adding a purchase transaction with an invalid foreign key.
        """
        db_manager_central = DatabaseManagerCentral(
            host=self.host, user=self.user, password=self.password, database=self.database
        )
    
        with patch.object(db_manager_central.instance_tables.users_profile, "search_record", return_value=False) as mock_user_search, \
             patch.object(db_manager_central.instance_tables.products_profile, "search_record", return_value=[{"id": "valid_product", "quantity": 10}]) as mock_product_search, \
             patch.object(db_manager_central.instance_tables.vending_machines_profile, "search_record", return_value=True) as mock_vm_search:
    
            user_id = "invalid_user"
            product_id = "valid_product"
            vending_machine_id = "valid_vm"
            quantity = 2
            amount_paid_per_unit = 10.0
    
            with self.assertRaises(ValueError) as context:
                db_manager_central.add_purchase_transaction(
                    user_id, product_id, vending_machine_id, quantity, amount_paid_per_unit
                )
    
            self.assertIn("Foreign key value 'invalid_user' does not exist", str(context.exception))
    
            mock_user_search.assert_called_once_with(user_id="invalid_user")
            mock_product_search.assert_called_once_with(id="valid_product")
    
        logger.info("Test add_purchase_transaction_invalid_foreign_key: OK!!! ---------------------------> TEST 8 OK!!!")
    


    def test_add_purchase_transaction_event_notify_failure(self):
        """
        Test failure to notify event during a purchase transaction.
        """
        db_manager_central = DatabaseManagerCentral(
            host=self.host, user=self.user, password=self.password, database=self.database
        )

        with patch.object(db_manager_central.instance_tables.purchase_transaction, "insert_row", return_value="transaction_id") as mock_insert_row, \
             patch.object(db_manager_central.instance_tables.users_profile, "search_record", return_value=True) as mock_user_search, \
             patch.object(db_manager_central.instance_tables.products_profile, "search_record", return_value=[{"id": "valid_product", "quantity": 10}]) as mock_product_search, \
             patch.object(db_manager_central.instance_tables.vending_machines_profile, "search_record", return_value=True) as mock_vm_search, \
             patch.object(db_manager_central._DatabaseManagerCentral__purchase_transaction_config_pub.event_manager, "notify", side_effect=Exception("Notify failure")) as mock_notify:

            user_id = "valid_user"
            product_id = "valid_product"
            vending_machine_id = "valid_vm"
            quantity = 2
            amount_paid_per_unit = 10.0

            with self.assertRaises(RuntimeError) as context:
                db_manager_central.add_purchase_transaction(
                    user_id, product_id, vending_machine_id, quantity, amount_paid_per_unit
                )

            self.assertIn("Failed to publish event", str(context.exception))

            mock_user_search.assert_called_with(user_id="valid_user")
            mock_product_search.assert_called_with(product_id="valid_product")
            mock_vm_search.assert_called_with(vending_machine_id="valid_vm")

            mock_insert_row.assert_called_once_with(
                user_id="valid_user", product_id="valid_product", vending_machine_id="valid_vm",
                quantity=2, amount_paid_per_unit=10.0
            )

            mock_notify.assert_called_once()
            logger.info("Test add_purchase_transaction_event_notify_failure: OK!!! ---------------------------> TEST 9 OK!!!")

    def test_add_product_quantity_success(self):
        """
        Test successful addition of product quantity.
        """
        db_manager_central = DatabaseManagerCentral(
            host=self.host, user=self.user, password=self.password, database=self.database
        )
    
        with patch.object(db_manager_central.products_profile, "get_by_id", return_value=["123", "Product A", "Description", 10.0, 50]) as mock_get_by_id, \
             patch.object(db_manager_central.products_profile, "update_row") as mock_update_row:

            product_id = "123"
            quantity_to_add = 20

            new_quantity = db_manager_central.add_product_quantity(product_id=product_id, quantity_to_add=quantity_to_add)

            self.assertEqual(new_quantity, 70)

            mock_get_by_id.assert_called_once_with(product_id)
            mock_update_row.assert_called_once_with(record_id="123", quantity=70)

        logger.info("Test add_product_quantity_success: OK!!! ---------------------------> TEST 10 OK!!!")


    def test_add_product_quantity_invalid_quantity(self):
        """
        Test adding product quantity with an invalid (non-positive) value.
        """
        db_manager_central = DatabaseManagerCentral(
            host=self.host, user=self.user, password=self.password, database=self.database
        )

        product_id = "123"
        quantity_to_add = 0  # Invalid quantity

        with self.assertRaises(ValueError) as context:
            db_manager_central.add_product_quantity(product_id=product_id, quantity_to_add=quantity_to_add)

        self.assertIn("The quantity to be added must be greater than zero", str(context.exception))
        logger.info("Test add_product_quantity_invalid_quantity: OK!!! ---------------------------> TEST 11 OK!!!")


    def test_add_product_quantity_not_found(self):
        """
        Test adding product quantity when the product is not found.
        """
        db_manager_central = DatabaseManagerCentral(
            host=self.host, user=self.user, password=self.password, database=self.database
        )

        with patch.object(db_manager_central.products_profile, "get_by_id", return_value=None) as mock_get_by_id:

            product_id = "invalid_product_id"
            quantity_to_add = 10

            with self.assertRaises(ValueError) as context:
                db_manager_central.add_product_quantity(product_id=product_id, quantity_to_add=quantity_to_add)

            self.assertIn("Product not found", str(context.exception))
            mock_get_by_id.assert_called_once_with(product_id)

        logger.info("Test add_product_quantity_not_found: OK!!! ---------------------------> TEST 12 OK!!!")

    def test_search_table_success(self):
        """
        Test successful search in a table.
        """
        db_manager_central = DatabaseManagerCentral(
            host=self.host, user=self.user, password=self.password, database=self.database
        )
    
        with patch.object(db_manager_central.products_profile, "search_record", return_value=[{"id": "1", "name": "Product A"}]) as mock_search_record:

            table_name = "products_profile"
            filters = {"id": "1"}

            records = db_manager_central.search_table(table_name, **filters)

            self.assertEqual(records, [{"id": "1", "name": "Product A"}])

            mock_search_record.assert_called_once_with(id="1")

        logger.info("Test search_table_success: OK!!! ---------------------------> TEST 13 OK!!!")


    def test_search_table_table_not_found(self):
        """
        Test searching in a table that does not exist.
        """
        db_manager_central = DatabaseManagerCentral(
            host=self.host, user=self.user, password=self.password, database=self.database
        )

        table_name = "invalid_table"
        filters = {"id": "1"}

        with self.assertRaises(ValueError) as context:
            db_manager_central.search_table(table_name, **filters)

        self.assertIn("Table 'invalid_table' not found", str(context.exception))
        logger.info("Test search_table_table_not_found: OK!!! ---------------------------> TEST 14 OK!!!")

    def test_search_table_search_failure(self):
        """
        Test search failure in the specified table due to an internal exception.
        """
        db_manager_central = DatabaseManagerCentral(
            host=self.host, user=self.user, password=self.password, database=self.database
        )
    
        with patch.object(db_manager_central.products_profile, "search_record", side_effect=Exception("Error fetching from table 'products_profile'")) as mock_search_record:
            table_name = "products_profile"
            filters = {"id": "1"}

            with self.assertRaises(Exception) as context:
                db_manager_central.search_table(table_name, **filters)

            self.assertIn("Error fetching from table 'products_profile'", str(context.exception))
            mock_search_record.assert_called_once_with(id="1")

        logger.info("Test search_table_search_failure: OK!!! ---------------------------> TEST 15 OK!!!")

    def test_get_sales_report(self):
        """
        Test the get_sales_report method for generating a sales report.
        """
        db_manager_central = DatabaseManagerCentral(
            host=self.host, user=self.user, password=self.password, database=self.database
        )
    
        mock_sales_data = [
            {"product_id": "prod_1", "total_sold": 100},
            {"product_id": "prod_2", "total_sold": 50},
        ]

        with patch.object(db_manager_central.purchase_transaction, "execute_sql", return_value=mock_sales_data) as mock_execute_sql:
            start_date = "2024-01-01"
            end_date = "2024-12-31"

            sales_report = db_manager_central.get_sales_report(start_date, end_date)

            expected_query = """
                SELECT product_id, SUM(quantity) as total_sold
                FROM purchase_transaction
                WHERE timestamp BETWEEN %s AND %s
                GROUP BY product_id
                ORDER BY total_sold DESC;
            """

            mock_execute_sql.assert_called_once_with(
                expected_query,
                params=(start_date, end_date),
                fetch_all=True
            )
            self.assertEqual(sales_report, mock_sales_data)
            logger.info("Test get_sales_report: OK!!! ---------------------------> TEST 16 OK!!!")


if __name__ == "__main__":
    unittest.main()