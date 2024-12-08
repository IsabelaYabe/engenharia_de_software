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

    def update(self, data):
        """
        Executes the update logic for the "PurchaseProductEvent".

        Args:
            data (dict): A dictionary containing the event data, expected to have the following keys:
                - `name` (str): The id of the product to update.
                - `vending_machine_id` (str): The ID of the vending machine where the product is located.
                - `quantity` (int): The quantity of the product being purchased.

        Logs:
            - Logs an info message before the update operation begins.
            - Logs a warning if the product is not found in the vending machine.
            - Logs a warning if the requested quantity is greater than the available quantity.
            - Logs a debug message with the product records retrieved.
            - Logs an info message when the product quantity is successfully updated.
            - Logs an error message if an exception occurs.

        Raises:
            Exception: If an error occurs during the update process.
        """
        logger.info(f"Executing update strategy with data: {data}")
        
        name = data["product_id"]
        vending_machine_id = data["vending_machine_id"]
        quantity = data["quantity"]
        try:
            existing_records = self.search_record(name=name, vending_machine_id=vending_machine_id)
            
            if not existing_records:
                logger.warning(f"Product '{name}' not found in vending machine '{vending_machine_id}'. Purchase aborted.")
                return
            
            logger.debug(f"Records: {existing_records}")   
            existing_product = existing_records[0]
            existing_id = existing_product["id"]  
            existing_quantity = existing_product["quantity"]
            if quantity > existing_quantity:
                logger.warning(f"Insufficient stock for product '{name}' in vending machine '{vending_machine_id}'. Available: {existing_quantity}, Requested: {quantity}")
                return       

            new_quantity = existing_quantity - quantity
            self.update_row(existing_id, quantity=new_quantity)

            logger.info(f"Purchase successful. Updated product '{name}' in vending machine '{vending_machine_id}' to new quantity: {new_quantity}")
        
        except Exception as e:
            logger.error(f"Failed to update product '{name}' in vending machine '{vending_machine_id}': {e}")
            raise