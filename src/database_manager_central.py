"""
    Module for creating the DatabaseManagerCentral class.

    Author: Isabela Yabe

    Last Modified: 15/10/2024

    Dependencies:
        - product_profile
        - decorators
        - tables
"""
from enum_tables import Tables
from product_profile import ProductProfile
from decorators import singleton

@singleton
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
        self.__host = host
        self.__user = user
        self.__password = password
        self.__database = database
        self.__tables = {self.__product_manager.table_name: self.__product_manager}
        self.__product_manager = ProductProfile(self.host, self.user, self.password, self.database)
        self._create_all_tables()

    def _create_all_tables(self):
        """
        Creates all the necessary tables in the database.
        """
        self.__product_manager._create_table()
    
    def _drop_all_tables(self):
        """
        Drops all tables from the database.
        """
        self.__product_manager._drop_table()

    def _reset_database(self):
        """
        Resets the database by dropping all tables and then recreating them.
        """
        self._drop_all_tables()
        self._create_all_tables()

    def _add_instance(self, table_manager, **instance_data):
        """
        Adds an instance to a table managed by the given table_manager.

        Parameters:
            table_manager (object): The table_manager class handling the instance (e.g., ProductProfile).
            **instance_data: Arbitrary keyword arguments representing the data of the instance.

        Returns:
            bool: True if the instance was added, False otherwise.
        """
        try:
            create_method = getattr(table_manager, "create_" + table_manager.table_name)  
            create_method(**instance_data)
            return True
        except AttributeError:
            print(f"The table_manager for table {table_manager.table_name} does not support this operation.")
            return False
        
    def _update(self, table_manager, **intances_data):
        self.__product_manager._update(**intances_data)