"""
Module for StockProfile class.

This module provides a class for managing stock information related to products 
and their associated vending machines in a MySQL database.

Author: Lavinia Dias

Date: 17/10/20224
"""

import mysql.connector

class StockProfile:
    """
    StockProfile class.

    This class manages the connection to a MySQL database and provides methods 
    for retrieving stock information about products and their vending machines.

    Attributes:
    - connection (mysql.connector.connection): A connection object to the MySQL database.
    - cursor (mysql.connector.cursor): A cursor object for executing SQL queries.

    Methods:
    - get_stock_info(self): Retrieves stock information for all products and their vending machines.
    - close(self): Closes the database connection.
    """
    
    def __init__(self, host, user, password, database):
        """
        Constructor for the StockProfile class.
        
        Parameters:
            host (str): The MySQL server host.
            user (str): The MySQL user.
            password (str): The MySQL user's password.
            database (str): The name of the MySQL database to connect to.
        """
        self.__connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.__cursor = self.__connection.cursor()

    def get_stock_info(self):
        """
        Retrieves stock information for all products and their vending machines.

        Returns:
            list: A list of dictionaries containing stock details, with each 
                  dictionary representing a product's stock information.
        """
        query = """
        SELECT 
            p.id AS product_id, 
            p.name AS product_name, 
            p.price AS product_price,
            p.quantity AS product_quantity,
            p.vending_machine_id AS vending_machine_id,
            vm.name AS vending_machine_name
        FROM 
            Products AS p
        JOIN 
            VendingMachines AS vm ON p.vending_machine_id = vm.id
        """
        self.__cursor.execute(query)
        stock_info = self.__cursor.fetchall()
        
        return [
            {
                'product_id': row[0],
                'product_name': row[1],
                'product_price': row[2],
                'product_quantity': row[3],
                'vending_machine_id': row[4],
                'vending_machine_name': row[5]
            }
            for row in stock_info
        ]

    def close(self):
        """Closes the database connection."""
        self.__cursor.close()
        self.__connection.close()


if __name__ == "__main__":
    db_config = {
        "host": "localhost",
        "user": "root",
        "password": "Alacazumba123*",
        "database": "my_database"
    }
    stock_profile = StockProfile(**db_config)
    stock_info = stock_profile.get_stock_info()
    for stock in stock_info:
        print(stock)

    stock_profile.close()
