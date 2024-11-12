"""
Module for ProductProfile Class.

This module defines the `ProductProfile` class, a subclass of `DatabaseManager`, designed to handle CRUD operations on a product profile database table. The `ProductProfile` class manages the `products` table, where each product has a unique ID, name, description, price, and quantity.

Author: Isabela Yabe
Last Modified: 11/11/2024
Status: Complete, put logs

Dependencies:
    - uuid
    - database_manager.DatabaseManager

Classes:
    - ProductProfile: Manages CRUD operations for product profiles in the `products` table.
"""

import uuid
from database_manager import DatabaseManager

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.getcwd(),'src')))
from decorators import immutable_fields

class ProductProfile(DatabaseManager):
    """
    ProductProfile class.

    This class provides CRUD functionality for managing product profiles in the `products` table. It inherits from 
    `DatabaseManager` and implements methods to create the table, insert new products, update existing ones, 
    delete products, and retrieve product details by ID.

    Attributes:
        - columns (list): List of column names for the `products` table, used for record retrieval.

    Methods:
        - _create_table(): Creates the `products` table if it does not exist.
        - insert_row(name, description, price, quantity): Inserts a new product into the table.
        - update_row(record_id, **kwargs): Updates product details based on the given product ID.
        - delete_row(record_id): Deletes a product from the table based on the given product ID.
        - get_by_id(id): Retrieves product details by ID.
    """

    def __init__(self, host, user, password, database):
        """
        Initializes the ProductProfile instance, setting up the connection and creating the `products` table if it 
        does not exist.

        Args:
            host (str): The MySQL server host.
            user (str): The MySQL user.
            password (str): The MySQL user's password.
            database (str): The name of the MySQL database.
        """
        super().__init__(host, user, password, database, "products")
        self.columns = ["id", "name", "description", "price", "quantity"]

    def get_column_id(self): 
        return "id"
    
    def _create_table(self):
        """
        Creates the `products` table with columns for ID, name, description, price, and quantity. If the table already 
        exists, it is not recreated.
        """
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS products (
            id VARCHAR(36) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            description TEXT,
            price DECIMAL(10, 2) NOT NULL,
            quantity INT NOT NULL
        );
        """
        self._create_table_(create_table_sql)

    def insert_row(self, name, description, price, quantity):
        """
        Inserts a new product into the `products` table.

        Args:
            name (str): The name of the product.
            description (str): A description of the product.
            price (float): The price of the product.
            quantity (int): The available quantity of the product.

        Returns:
            str: The ID of the newly created product.
        """
        product_id = str(uuid.uuid4())
        self._insert_row(id=product_id, name=name, description=description, price=price, quantity=quantity)
        return product_id
    
    @immutable_fields(['id'])
    def update_row(self, record_id, **kwargs):
        """
        Updates an existing product's details in the `products` table.

        Args:
            record_id (str): The ID of the product to update.
            **kwargs: The columns and values to update for the product.
        """
        return self._update_row(record_id, "id", **kwargs)
    
    def delete_row(self, record_id):
        """
        Deletes a product from the `products` table by ID.

        Args:
            record_id (str): The ID of the product to delete.
        """
        return self._delete_row(record_id, "id")
    
    def get_by_id(self, record_id):
        """
        Retrieves a product by its ID, returning all details (id, name, description, price, quantity).

        Args:
            id (str): The ID of the product to retrieve.

        Returns:
            dict: A dictionary with the product details, or None if the product is not found.
        """       
        record = self._get_by_id(record_id, "id")

        if record is None:
            return None
        
        row = {}
        count = 0
        for value in record:
            row[self.columns[count]] = value
            count+=1
        return row