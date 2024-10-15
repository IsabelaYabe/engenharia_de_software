"""
    Module for creating the ProductProfile class.

    Authoir: Isabela Yabe

    Last Modified: 15/10/2024

    Dependencies: 
        - uuid
        - util
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
        Constructor for the ProductProfileDB class.
        
        Parameters:
            host (str): The MySQL server host.
            user (str): The MySQL user.
            password (str): The MySQL user's password.
            database (str): The name of the MySQL database.

        Returns:
            None
        """
        super().__init__(host, user, password, database, "products")
        self.__create_table()
    
        def __create_table(self):
            """
            Creates the products table in the MySQL database.
            """
            create_table_sql = '''
            CREATE TABLE IF NOT EXISTS products (
                product_id CHAR(36) PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                description TEXT,
                price DECIMAL(10, 2) NOT NULL,
                review INT(1) DEFAULT 0
            );
            '''
            self._create_table(create_table_sql)

    def create_product(self, name, description, price):
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
        conn = mysql.connector.connect(**self.db_config)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO products (product_id, name, description, price, review) VALUES (%s, %s, %s, %s, %s)',
                       (product_id, name, description, price, 0))
        conn.commit()
        cursor.close()
        conn.close()
        return product_id
    
    def get_product(self, product_id):
        """
        Retrieves a product by its ID from the database.

        Parameters:
            product_id (str): The ID of the product.

        Returns:
            product (dict): A dictionary with the product details, or None if not found.
        """
        conn = mysql.connector.connect(**self.db_config)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM products WHERE product_id = %s', (product_id,))
        product = cursor.fetchone()
        cursor.close()
        conn.close()

        if product:
            return {'product_id': product[0], 'name': product[1], 'description': product[2], 'price': product[3]}
        return None

    def update_price(self, price):
        """
        Update the price for the product, ensuring it is valid.

        Parameters:
            price (float): The price of the product.

        Returns:
            None
        """


    def update_name(self, name):
        """
        Update the name for the product, ensuring it is valid.	

        Parameters:
            name (str): The name of the product.

        Returns:
            None
        """


    def update_description(self, description):
        """
        Update the description for the product, ensuring it is valid.

        Parameters:
            description (str): The description of the product.

        Returns:
            None
        """
    def update_review(self, review):
        """
        Update the review for the product, ensuring it is valid.

        Parameters:
            review (int): The review of the product.

        Returns:
            None
        """

    def delete_product(self):
        """
        Delete the product, setting its attributes to None.

        Parameters:
            None

        Returns:
            None
        """