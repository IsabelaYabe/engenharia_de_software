"""
Module for StockProfile class.

This module provides a class for managing vending machine information in a MySQL database.

Author: Rodrigo Kalil

Date: 24/10/20224
"""

import mysql.connector

class VMProfile:
    """
    VMProfile class.

    This class provides methods for retrieving vending machine information from a MySQL database.

    Attributes:
        __connection (mysql.connector.connection.MySQLConnection): The connection to the MySQL database.
        __cursor (mysql.connector.cursor.MySQLCursor): The cursor to the MySQL database.
    """
    
    def __init__(self, host, user, password, database):
        """
        Initializes the VMProfile object.

        Args:
            host (str): The host of the MySQL database.
            user (str): The user of the MySQL database.
            password (str): The password of the MySQL database.
            database (str): The database name.
        """
        self.__connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.__cursor = self.__connection.cursor()

    def get_vm_info(self):
        """
        Retrieves the vending machine information from the database.

        Returns:
            list[dict]: A list of dictionaries containing the vending machine information.
        """
        query = """
        SELECT 
            vm.VMID,
            vm.Name,
            vm.Location,
            vm.OwnerID,
            vm.Status
        FROM 
            VMs as vm
        """
        self.__cursor.execute(query)
        vm_info = self.__cursor.fetchall()
        
        return [
            {
                "VMID": row[0],
                "Name": row[1],
                "Location": row[2],
                "OwnerID": row[3],
                "Status": row[4]
            }
            for row in vm_info
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
    vm_profile = VMProfile(**db_config)
    vm_info = vm_profile.get_vm_info()
    for vm in vm_info:
        print(vm)

    vm_profile.close()
