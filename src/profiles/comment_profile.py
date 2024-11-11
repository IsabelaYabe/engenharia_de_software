"""
Module for CommentProfile Class.

This module defines the `CommentProfile` class, a specialized implementation of the `DatabaseManager` abstract class. 
The `CommentProfile` class manages comments in a database, allowing for the creation, retrieval, updating, and deletion of comment records. 
The class enforces immutability on specified fields through the use of a decorator, ensuring data integrity for `id` and `timestamp` fields.

Author: Isabela Yabe
Last Modified: 10/11/2024
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

class CommentProfile(DatabaseManager):
    """
    CommentProfile class.

    This class extends `DatabaseManager` and provides an interface for managing comments in a SQL database.
    It implements CRUD operations specifically for a "comments" table and enforces immutability on specified fields
    (e.g., `id`, `timestamp`) using the `immutable_fields` decorator.

    Attributes:
        - columns (list): List of column names in the "comments" table.

    Methods:
        - insert_row(text): Inserts a new comment with a unique ID and returns the ID.
        - update_row(record_id, **kwargs): Updates fields for a specific comment while enforcing immutability on specified fields.
        - delete_row(record_id): Deletes a comment by its ID.
        - get_by_id(id): Retrieves a comment record by ID, returning it as a dictionary.
    """
    def __init__(self, host, user, password, database):
        """
        Initializes the CommentProfile instance and creates the "comments" table if it does not exist.

        Args:
            host (str): The database server's hostname or IP address.
            user (str): The username for authenticating with the database.
            password (str): The password for the specified user.
            database (str): The name of the database to connect to.
        """
        super().__init__(host, user, password, database, "comments")
        self.columns = ["id", "text", "timestamp"]
        self._create_table()

    def _create_table(self):
        """
        Creates the "comments" table in the database with the following structure:
            - id: A unique identifier for the comment (UUID format).
            - text: The content of the comment (required).
            - timestamp: A timestamp indicating when the comment was created or last updated.

        This method only executes the table creation if the table does not already exist.
        """
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS comments (
            id VARCHAR(36) PRIMARY KEY,
            text VARCHAR(255) NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        );
        """
        self._create_table_(create_table_sql)

    def insert_row(self, text):
        """
        Inserts a new comment into the "comments" table with a unique ID.

        Args:
            text (str): The content of the comment.

        Returns:
            str: The unique ID of the inserted comment (UUID format).
        """
        comment_id = str(uuid.uuid4())
        self._insert_row(
            id=comment_id, text=text
            )
        return comment_id
    
    @immutable_fields(['id', 'timestamp'])
    def update_row(self, record_id, **kwargs):
        """
        Updates the fields of a comment in the "comments" table, enforcing immutability on specified fields.

        This method updates the specified fields for a comment record, except for immutable fields (`id` and `timestamp`).

        Args:
            record_id (str): The ID of the comment to update.
            **kwargs: Key-value pairs representing the fields and their new values.

        Returns:
            None
        """
        return self._update_row(record_id, "id", **kwargs)
    
    def delete_row(self, record_id):
        """
        Deletes a comment from the "comments" table based on its ID.

        Args:
            record_id (str): The ID of the comment to delete.

        Returns:
            None
        """
        return self._delete_row(record_id, "id")
    
    def get_by_id(self, id):
        """
        Retrieves a comment by its ID and returns it as a dictionary.

        This method fetches the comment record from the database and formats it as a dictionary with field names as keys.

        Args:
            id (str): The unique ID of the comment to retrieve.

        Returns:
            dict or None: A dictionary containing the comment's data if found, or None if not found.
        """
        record = self._get_by_id(id, "id")

        if record is None:
            return None
        
        row = {}
        count = 0
        for value in record:
            row[self.columns[count]] = value
            count+=1
        return row