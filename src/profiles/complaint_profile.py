"""
Module for ComplaintProfile Class.

This module defines the `ComplaintProfile` class, a specialized implementation of the `DatabaseManager` abstract class. 
The `ComplaintProfile` class manages complaints in a database, allowing for the creation, retrieval, updating, and deletion of complaint records. 
The class enforces immutability on specified fields through the use of a decorator, ensuring data integrity for `id` and `timestamp` fields.

Author: Isabela Yabe
Last Modified: 11/11/2024
Status: Complete, put logs

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

class ComplaintProfile(DatabaseManager):
    """
    ComplaintProfile class.

    This class extends `DatabaseManager` and provides an interface for managing complaints in a SQL database.
    It implements CRUD operations specifically for a "complaints" table and enforces immutability on specified fields
    (e.g., `id`, `timestamp`) using the `immutable_fields` decorator.

    Attributes:
        - columns (list): List of column names in the "complaints" table.

    Methods:
        - insert_row(text): Inserts a new complaint with a unique ID and returns the ID.
        - update_row(record_id, **kwargs): Updates fields for a specific complaint while enforcing immutability on specified fields.
        - delete_row(record_id): Deletes a complaint by its ID.
        - get_by_id(id): Retrieves a complaint record by ID, returning it as a dictionary.
    """
    def __init__(self, host, user, password, database):
        """
        Initializes the ComplaintProfile instance and creates the "complaints" table if it does not exist.

        Args:
            host (str): The database server's hostname or IP address.
            user (str): The username for authenticating with the database.
            password (str): The password for the specified user.
            database (str): The name of the database to connect to.
        """
        super().__init__(host, user, password, database, "complaints")
        self.columns = ["id", "text", "timestamp"]
    
    def get_column_id(self): 
        return "id"
    
    def _create_table(self):
        """
        Creates the "complaints" table in the database with the following structure:
            - id: A unique identifier for the complaint (UUID format).
            - text: The content of the complaint (required).
            - timestamp: A timestamp indicating when the complaint was created or last updated.

        This method only executes the table creation if the table does not already exist.
        """
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS complaints (
            id VARCHAR(36) PRIMARY KEY,
            text VARCHAR(255) NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        );
        """
        self._create_table_(create_table_sql)

    def insert_row(self, text):
        """
        Inserts a new complaint into the "complaints" table with a unique ID.

        Args:
            text (str): The content of the complaint.

        Returns:
            str: The unique ID of the inserted complaint (UUID format).
        """
        complaint_id = str(uuid.uuid4())
        self._insert_row(
            id=complaint_id, text=text
            )
        return complaint_id
    
    @immutable_fields(['id', 'timestamp'])
    def update_row(self, record_id, **kwargs):
        """
        Updates the fields of a complaint in the "complaints" table, enforcing immutability on specified fields.

        This method updates the specified fields for a complaint record, except for immutable fields (`id` and `timestamp`).

        Args:
            record_id (str): The ID of the complaint to update.
            **kwargs: Key-value pairs representing the fields and their new values.

        Returns:
            None
        """
        return self._update_row(record_id, "id", **kwargs)
    
    def delete_row(self, record_id):
        """
        Deletes a complaint from the "complaints" table based on its ID.

        Args:
            record_id (str): The ID of the complaint to delete.

        Returns:
            None
        """
        return self._delete_row(record_id, "id")
    
    def get_by_id(self, record_id):
        """
        Retrieves a complaint by its ID and returns it as a dictionary.

        This method fetches the complaint record from the database and formats it as a dictionary with field names as keys.

        Args:
            id (str): The unique ID of the complaint to retrieve.

        Returns:
            dict or None: A dictionary containing the complaint's data if found, or None if not found.
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