"""
Module for defining subscriber update strategies.

This module provides an abstract base class `SubUpdateStrategy` and three concrete 
implementations: `DefaultSubUpdateStrategy`, `PurchaseProductSubUpdateStrategy`, 
and `WithdrawSubUpdateStrategy`.

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
        """

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
    Implementation of the `SubUpdateStrategy` interface for handling product purchases.

    This strategy updates product quantities in vending machines, user budgets, 
    and the vending machine's budget after a purchase event.
    """

    def update(self, data, table_name, search_record, update_row):
        """
        Executes the update logic for a product purchase.

        Args:
            data (dict): A dictionary containing the purchase data.
            table_name (str): The name of the table being updated.
            search_record (function): A function to search for existing records.
            update_row (function): A function to update a row in the database.
        """
        quantity = data["quantity"]
        
        if table_name == "products_profile":
            
            product = data["product_id"]
            vending_machine_id = data["vending_machine_id"]
            
            try:
                existing_records = search_record(id=product, vending_machine_id=vending_machine_id)

                if not existing_records:
                    logger.warning(f"Product '{product}' not found in vending machine '{vending_machine_id}'. Purchase aborted.")
                    return
  
                existing_product = existing_records[0]
                existing_id = existing_product[0]  
                existing_quantity = existing_product[4] 

                new_quantity = existing_quantity - quantity
                update_row(existing_id, quantity=new_quantity)

                logger.info(f"Purchase successful. Updated product '{product}' in vending machine '{vending_machine_id}' to new quantity: {new_quantity}")
            except Exception as e:
                logger.error(f"Failed to update product '{product}' in vending machine '{vending_machine_id}': {e}")
                raise

        elif table_name == "vending_machines_profile":

            vending_machine = data["vending_machine_id"]
            new_budget = quantity*data["amount_paid_per_unit"]
            
            try:
                existing_records = search_record(id=vending_machine)

                if not existing_records:
                    logger.warning(f"Vending machine '{vending_machine}' not found. Purchase aborted.")
                    return
                
                existing_product = existing_records[0]
                existing_id = existing_product[0]
                old_budget = existing_product[4]

                update_row(existing_id, budget=new_budget+old_budget)

                logger.info(f"Updated budget for vending machine '{vending_machine}' to: {new_budget+old_budget}")
            except Exception as e:
                logger.error(f"Failed to update budget for vending machine '{vending_machine}': {e}")
                raise

        elif table_name == "users_profile":
            
            user = data["user_id"]
            new_budget = quantity*data["amount_paid_per_unit"]
            
            try:
                existing_records = search_record(id=user)
                if not existing_records:
                    logger.warning(f"User '{user}' not found. Purchase aborted.")
                    return
                
                existing_user = existing_records[0]
                existing_id = existing_user[0]
                old_budget = existing_user[9]
                
                update_row(existing_id, budget=old_budget-new_budget)
                
                logger.info(f"Updated budget for user '{user}' to: {new_budget+old_budget}")
            except Exception as e:
                logger.error(f"Failed to update budget for user '{user}': {e}")
                raise

class WithdrawSubUpdateStrategy(SubUpdateStrategy):
    """
    Implementation of the `SubUpdateStrategy` interface for handling withdrawals from vending machines.

    This strategy updates the budget of a vending machine after a withdrawal event.
    """
    def update(self, data, table_name, search_record, update_row):
        """
        Executes the update logic for a withdrawal.

        Args:
            data (dict): A dictionary containing the withdrawal data.
            table_name (str): The name of the table being updated.
            search_record (function): A function to search for existing records.
            update_row (function): A function to update a row in the database.
        Logs:
            - Logs info messages before the update process begins.
            - Logs debug messages with data being processed.
            - Logs an error message if the update fails.
        """    
        if table_name == "vending_machines_profile":

            vending_machine = data["vending_machine_id"]
            new_budget = data["new_budget"]
            
            try:
                update_row(vending_machine, budget=new_budget)

                logger.info(f"Updated budget for vending machine '{vending_machine}' to: {new_budget}")
            except Exception as e:
                logger.error(f"Failed to update budget for vending machine '{vending_machine}': {e}")
                raise