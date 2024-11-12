"""
Module for VMProfile Class.

This module defines the `VMProfile` class, a specialized implementation of the `DatabaseManager` abstract class. 
The `VMProfile` class manages vending machines in a database, allowing for the creation, retrieval, updating, and deletion of vending machine records. 

Author: Isabela Yabe
Last Modified: 11/11/2024
Status: To testing, put logs

Dependencies:
    - uuid
    - database_manager.DatabaseManager
    - decorators.immutable_fields
"""
import uuid
from database_manager import DatabaseManager

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.getcwd(),'src')))
from decorators import immutable_fields

class VMProfile(DatabaseManager):
    """
    VMProfile class.

    This class extends `DatabaseManager` and provides an interface for managing vending machines in a SQL database.
    It implements CRUD operations specifically for a "vending machines" table and enforces immutability on specified fields using the `immutable_fields` decorator.

    Attributes:
        - columns (list): List of column names in the "vending machines" table.

    Methods:
        - insert_row(text): Inserts a new vending machine with a unique ID and returns the ID.
        - update_row(record_id, **kwargs): Updates fields for a specific vending machine while enforcing immutability on specified fields.
        - delete_row(record_id): Deletes a vending machine by its ID.
        - get_by_id(id): Retrieves a vending machine record by ID, returning it as a dictionary.
    """
    def __init__(self, host, user, password, database):
        """
        Initializes the VMProfile instance and creates the "vending machines" table if it does not exist.

        Args:
            host (str): The database server's hostname or IP address.
            user (str): The username for authenticating with the database.
            password (str): The password for the specified user.
            database (str): The name of the database to connect to.
        """
        super().__init__(host, user, password, database, "vending machines")
        self.columns = ["id", "name", "location", "status"]

    def get_column_id(self): 
        return "id"
    
    def _create_table(self):
        """
        Creates the "vending machines" table in the database with the following structure:
            - id: A unique identifier for the vending machine (UUID format).
            - text: The content of the vending machine (required).
            - timestamp: A timestamp indicating when the vending machine was created or last updated.

        This method only executes the table creation if the table does not already exist.
        """
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS `vending machines` (
            id VARCHAR(36) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            location VARCHAR(255) NOT NULL,
            status VARCHAR(255) NOT NULL
        );
        """
        self._create_table_(create_table_sql)

    def insert_row(self, name, location, status):
        """
        Inserts a new vending machine into the "vending machines" table with a unique ID.

        Args:
            text (str): The content of the vending machine.

        Returns:
            str: The unique ID of the inserted vending machine (UUID format).
        """
        vending_machine_id = str(uuid.uuid4())
        self._insert_row(
            id=vending_machine_id, name=name, location=location, status=status
            )
        return vending_machine_id
    
    @immutable_fields(['id'])
    def update_row(self, record_id, **kwargs):
        """
        Updates the fields of a vending machine in the "vending machines" table, enforcing immutability on specified fields.

        This method updates the specified fields for a vending machine record, except for immutable fields (`id`).

        Args:
            record_id (str): The ID of the vending machine to update.
            **kwargs: Key-value pairs representing the fields and their new values.

        Returns:
            None
        """
        return self._update_row(record_id, "id", **kwargs)
    
    def delete_row(self, record_id):
        """
        Deletes a vending machine from the "vending machines" table based on its ID.

        Args:
            record_id (str): The ID of the vending machine to delete.

        Returns:
            None
        """
        return self._delete_row(record_id, "id")
    
    def get_by_id(self, record_id):
        """
        Retrieves a vending machine by its ID and returns it as a dictionary.

        This method fetches the vending machine record from the database and formats it as a dictionary with field names as keys.

        Args:
            id (str): The unique ID of the vending machine to retrieve.

        Returns:
            dict or None: A dictionary containing the vending machine's data if found, or None if not found.
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