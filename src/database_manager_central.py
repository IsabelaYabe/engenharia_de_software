"""
    Module for creating the DataManagerCentral class.

    Authoir: Isabela Yabe

    Last Modified: 15/10/2024

    Dependencies:
        - uuid
        - utils
        - mysql.connector
"""

from product_profile import ProductProfile

class DatabaseManagerCentral:
    """
    DatabaseManagerCentral class.
    
    This class provides a central manager for all the individual table managers.
    """

    def __init__(self, host, user, password, database):
        """
        Initializes the central manager with table-specific managers.
        
        Parameters:
            host (str): The MySQL server host.
            user (str): The MySQL user.
            password (str): The MySQL user's password.
            database (str): The name of the MySQL database.
        """
        self.product_manager = ProductProfile(host, user, password, database)
    
    def _create_all_tables(self):
        """
        Creates all the necessary tables in the database.
        """
        self.product_manager._create_table()
    
    def _drop_all_tables(self):
        """
        Drops all tables from the database.
        """
        pass

    def _reset_database(self):
        """
        Resets the database by dropping all tables and then recreating them.
        """
        pass

    def _add_instance(self, manager, **instance_data):
        """
        Adds an instance to a table managed by the given manager.

        Parameters:
            manager (object): The manager class handling the instance (e.g., ProductProfile).
            **instance_data: Arbitrary keyword arguments representing the data of the instance.

        Returns:
            bool: True if the instance was added, False otherwise.
        """
        try:
            create_method = getattr(manager, "create_" + manager.table_name.rstrip('s'))  
            create_method(**instance_data)
            return True
        except AttributeError:
            print(f"The manager for table {manager.table_name} does not support this operation.")
            return False