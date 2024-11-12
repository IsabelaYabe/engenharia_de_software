"""
Module for UserProfile Class.

This module defines the `UserProfile` class, a specialized implementation of the `DatabaseManager` abstract class. 
The `UserProfile` class manages users in a database, allowing for the creation, retrieval, updating, and deletion of user records. 

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

class UserProfile(DatabaseManager):
    """
    UserProfile class.

    This class extends `DatabaseManager` and provides an interface for managing users in a SQL database.
    It implements CRUD operations specifically for a "users" table and enforces immutability on specified fields using the `immutable_fields` decorator.

    Attributes:
        - columns (list): List of column names in the "users" table.

    Methods:
        - insert_row(text): Inserts a new user with a unique ID and returns the ID.
        - update_row(record_id, **kwargs): Updates fields for a specific user while enforcing immutability on specified fields.
        - delete_row(record_id): Deletes a user by its ID.
        - get_by_id(id): Retrieves a user record by ID, returning it as a dictionary.
    """
    def __init__(self, host, user, password, database):
        """
        Initializes the UserProfile instance and creates the "users" table if it does not exist.

        Args:
            host (str): The database server's hostname or IP address.
            user (str): The username for authenticating with the database.
            password (str): The password for the specified user.
            database (str): The name of the database to connect to.
        """
        super().__init__(host, user, password, database, "users")
        self.columns = ["id", "username", "email", "password", "first name", "last name", "birthdate", "phone number", "address"]

    def get_column_id(self): 
        return "id"
    
    def _create_table(self):
        """
        Creates the "users" table in the database with the following structure:
            - id: A unique identifier for the user (UUID format).
            - text: The content of the user (required).
            - timestamp: A timestamp indicating when the user was created or last updated.

        This method only executes the table creation if the table does not already exist.
        """
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS users (
            id VARCHAR(36) PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            email VARCHAR(255) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL,
            `first name` VARCHAR(50) NOT NULL, 
            `last name` VARCHAR(50) NOT NULL,
            birthdate DATE,
            `phone number` VARCHAR(20),
            address VARCHAR(255) NOT NULL
        );
        """
        self._create_table_(create_table_sql)

    def insert_row(self, username, email, password, first_name, last_name, birthdate, phone_number, address):
        """
        Inserts a new user into the "users" table with a unique ID.

        Args:
            text (str): The content of the user.

        Returns:
            str: The unique ID of the inserted user (UUID format).
        """
        user_id = str(uuid.uuid4())
        self._insert_row(
            id=user_id, username=username, email=email, password=password, first_name=first_name, last_name=last_name, birthdate=birthdate, phone_number=phone_number, address=address
            )
        return user_id
    
    @immutable_fields(['id', 'birthdate', 'first name', 'last name'])
    def update_row(self, record_id, **kwargs):
        """
        Updates the fields of a user in the "users" table, enforcing immutability on specified fields.

        This method updates the specified fields for a user record, except for immutable fields.

        Args:
            record_id (str): The ID of the user to update.
            **kwargs: Key-value pairs representing the fields and their new values.

        Returns:
            None
        """
        return self._update_row(record_id, "id", **kwargs)
    
    def delete_row(self, record_id):
        """
        Deletes a user from the "users" table based on its ID.

        Args:
            record_id (str): The ID of the user to delete.

        Returns:
            None
        """
        return self._delete_row(record_id, "id")
    
    def get_by_id(self, record_id):
        """
        Retrieves a user by its ID and returns it as a dictionary.

        This method fetches the user record from the database and formats it as a dictionary with field names as keys.

        Args:
            id (str): The unique ID of the user to retrieve.

        Returns:
            dict or None: A dictionary containing the user's data if found, or None if not found.
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