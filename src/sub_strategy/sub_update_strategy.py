"""
Module for defining subscriber update strategies.

This module provides an abstract base class `SubUpdateStrategy` and two concrete 
implementations: `DefaultSubUpdateStrategy` and `PurchaseProductSubUpdateStrategy`.

Author: Isabela Yabe
Last Modified: 07/12/2024
Status: Complete

Dependencies:
    - abc.ABC
    - abc.abstractmethod
    - custom_logger.setup_logger
"""

from abc import ABC, abstractmethod
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), 'src')))
from custom_logger import setup_logger

logger = setup_logger()

class SubUpdateStrategy(ABC):
    """
    Abstract base class for subscriber update strategies.

    This class defines the interface for updating subscribers based on event data.
    Any custom update strategy should inherit from this class and implement the `update` method.
    """
    @abstractmethod
    def update(self, data): 
        """
        Executes the update logic for a subscriber.

        Args:
            data (dict): A dictionary containing the data to be used in the update.

        Raises:
            NotImplementedError: If the subclass does not implement this method.
        """
        pass

class DefaultSubUpdateStrategy(SubUpdateStrategy):
    """
    Default implementation of the `SubUpdateStrategy` interface.

    This class provides a generic update method that can handle any type of data.
    It logs the process and raises exceptions for invalid operations.
    """

    def update(self, data):
        """
        Executes the default update logic with the provided data.

        Args:
            data (dict): A dictionary containing the data to be processed in the update.

        Logs:
            - Logs an info message before the update operation begins.
            - Logs a debug message with the data being processed.
            - Logs a success message if the update is successful.
            - Logs an error message if the update fails.

        Raises:
            ValueError: If the provided data is invalid.
            Exception: If an error occurs during the update process.
        """
        logger.info("Executing default update strategy...")
        
        if not isinstance(data, dict):
            logger.error("Invalid data type. Expected a dictionary.")
            raise ValueError("Data must be a dictionary.")

        logger.debug(f"Processing update with data: {data}")

        try:
            for key, value in data.items():
                logger.info(f"Updating field '{key}' to value '{value}'")

            logger.info("Default update strategy executed successfully.")
        except Exception as e:
            logger.error(f"Error occurred during default update: {e}")
            raise

class PurchaseProductSubUpdateStrategy(SubUpdateStrategy):
    """
    Implementation of the `SubUpdateStrategy` interface for the "PurchaseProductEvent".

    This strategy handles the logic of updating product quantities after a purchase event.
    It searches for the product in the vending machine, verifies the available quantity, 
    and updates the quantity if the purchase is valid.
    """

    def update(self, data, table_name, search_record, update_row):
        logger.info(f"Executing update strategy with data: {data}")
        logger.debug(f"Table name: {table_name}")
        if table_name == "products_profile":
            product = data["product_id"]
            vending_machine_id = data["vending_machine_id"]
            quantity = data["quantity"]
            try:
                existing_records = search_record(id=product, vending_machine_id=vending_machine_id)

                if not existing_records:
                    logger.warning(f"Product '{product}' not found in vending machine '{vending_machine_id}'. Purchase aborted.")
                    return

                logger.debug(f"Records: {existing_records}")   
                existing_product = existing_records[0]
                existing_id = existing_product[0]  
                existing_quantity = existing_product[4]
                if quantity > existing_quantity:
                    logger.warning(f"Insufficient stock for product '{product}' in vending machine '{vending_machine_id}'. Available: {existing_quantity}, Requested: {quantity}")
                    return       

                new_quantity = existing_quantity - quantity
                update_row(existing_id, quantity=new_quantity)

                logger.info(f"Purchase successful. Updated product '{product}' in vending machine '{vending_machine_id}' to new quantity: {new_quantity}")

            except Exception as e:
                logger.error(f"Failed to update product '{product}' in vending machine '{vending_machine_id}': {e}")
                raise

        elif table_name == "vending_machines_profile":
            vending_machine = data["vending_machine_id"]
            new_budget = data["quantity"]*data["amount_paid_per_unit"]
            logger.debug(f"Vending machine: {vending_machine}, New budget: {new_budget}")
            try:
                existing_records = search_record(id=vending_machine)
                old_budget = existing_records[0][4]
                update_row(
                    record_id=vending_machine,
                    budget=new_budget+old_budget
                )
                logger.info(f"Updated budget for vending machine '{vending_machine}' to: {new_budget+old_budget}")
            except Exception as e:
                logger.error(f"Failed to update budget for vending machine '{vending_machine}': {e}")
                raise

        elif table_name == "users_profile":
            user = data["user_id"]
            new_balance = data["amount_paid_per_unit"]*data["quantity"]
            logger.debug(f"User: {user}, New balance: {new_balance}")
            try:
                existing_records = search_record(id=user)
                old_balance = existing_records[0][9]
                update_row(
                    record_id=user,
                    balance=new_balance+old_balance
                )
                logger.info(f"Updated balance for user '{user}' to: {new_balance+old_balance}")
            except Exception as e:
                logger.error(f"Failed to update balance for user '{user}': {e}")
                raise