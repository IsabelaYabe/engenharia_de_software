"""
    Module for creating the ProductProfile class.

    Authoir: Isabela Yabe

    Last Modified: 15/10/2024

    Dependencies:
        - uuid
        - utils
        - mysql.connector
"""

import uuid
from database_manager import DatabaseManager
from utils import contains_banned_words
    

class ProductProfile(DatabaseManager):
    """
    ProductProfile class.
    
    This class acts as an interface for managing product records in a MySQL database.
    It provides methods for creating, updating, monitoring, and deleting products.

    Inherits from DatabaseManager to leverage common database operations.

    Attributes:
    - db_config (dict): A dictionary containing the MySQL database configuration.

    Methods:
    - create_product(self, name, description, price): Creates a new product in the database.
    - get_product(self, product_id): Retrieves a product by its ID.
    - update_price(self, product_id, price): Update the price for a product by its ID.
    - update_name(self, product_id, name): Update the name for a product by its ID.
    - update_description(self, product_id, description): Update the description for a product by its ID.
    - delete_product(self, product_id): Delete a product from the database.
    """
    def __init__(self, host, user, password, database):
        """
        Constructor for the ProductProfile class.
        
        Parameters:
            host (str): The MySQL server host.
            user (str): The MySQL user.
            password (str): The MySQL user's password.
            database (str): The name of the MySQL database.
        """
        super().__init__(host, user, password, database, "products")
        self._create_table()

    def _create_table(self):
        """
        Creates the products table in the database if it doesn't exist.
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
        super()._create_table(create_table_sql)

    def create_product(self, name, description, price, quantity):
        """
        Creates a new product in the database.
        
        Parameters:
            name (str): The name of the product.
            description (str): The description of the product.
            price (float): The price of the product.

        Returns:
            product_id (str): The ID of the newly created product.
        """
        product_id = str(uuid.uuid4())
        self._insert_row(
            columns=["product_id", "name", "description", "price", "quantity"],
            values=(product_id, name, description, price, quantity)
        )
        return product_id
    
    def get_product(self, product_id):
        """
        Retrieves a product by its ID, returning all details (id, name, description, price, quantity).
        
        Parameters:
            product_id (str): The ID of the product.

        Returns:
            dict: A dictionary with all the product details, or None if not found.
        """
        conn = self._connect()
        cursor = conn.cursor()

        query = f'SELECT id, name, description, price, quantity FROM {self.table_name} WHERE id = %s'
        cursor.execute(query, (product_id,))
        record = cursor.fetchone()
        cursor.close()
        conn.close()

        if record:
            return {
                "product_id": record[0],
                "name": record[1],
                "description": record[2],
                "price": record[3],
                "quantity": record[4]
            }
        return None

    def update_price(self, product_id, price):
        """
        Update the price for a product by its ID.

        Parameters:
            product_id (str): The ID of the product.
            price (float): The new price of the product.

        Returns:
            None
        """
        self._update_row({"price": price}, f"product_id = '{product_id}'")


    def update_name(self, product_id, name):
        """
        Update the name for a product by its ID.

        Parameters:
            product_id (str): The ID of the product.
            name (str): The new name of the product.

        Returns:
            None
        """
        self._update_row({"name": name}, f"product_id = '{product_id}'")


    def update_description(self, product_id, description):
        """
        Update the description for a product by its ID.

        Parameters:
            product_id (str): The ID of the product.
            description (str): The new description of the product.

        Returns:
            None
        """
        self._update_row({"description": description}, f"product_id = '{product_id}'")

    def delete_product(self, product_id):
        """
        Delete a product from the database.

        Parameters:
            product_id (str): The ID of the product to delete.

        Returns:
            None
        """
        self._delete_row(product_id)