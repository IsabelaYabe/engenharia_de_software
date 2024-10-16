"""
Module for creating the CommentProfile class.

Author: Lavínia Dias

Last Modified: 16/10/2024

Dependencies: 
    - uuid
    - mysql.connector
    - utils (contains_banned_words)
"""

import uuid
import mysql.connector
from database_manager import DatabaseManager
from utils import contains_banned_words
    

class CommentProfile(DatabaseManager):
    """
    CommentProfile class.
    
    This class acts as an interface for managing comment records in a MySQL database.
    It provides methods for creating, updating, retrieving, and deleting comments.

    Inherits from DatabaseManager to leverage common database operations.

    Attributes:
    - db_config (dict): A dictionary containing the MySQL database configuration.

    Methods:
    - create_comment(self, product_id, user_id, text): Creates a new comment in the database associated with a product and a user.
    - get_comment(self, comment_id): Retrieves a comment by its ID.
    - get_comments_by_product(self, product_id): Retrieves all comments associated with a product.
    - delete_comment(self, comment_id): Deletes a comment from the database.
    """
    def __init__(self, host, user, password, database):
        """
        Constructor for the CommentProfile class.
        
        Parameters:
            host (str): The MySQL server host.
            user (str): The MySQL user.
            password (str): The MySQL user's password.
            database (str): The name of the MySQL database.

        Returns:
            None
        """
        super().__init__(host, user, password, database, "comments")
        self.__create_table()

    def __create_table(self):
        """
        Creates the comments table in the MySQL database if it does not already exist.
        The table stores comments along with the product_id and user_id they are associated with.
        """
        create_table_sql = '''
        CREATE TABLE IF NOT EXISTS comments (
            comment_id CHAR(36) PRIMARY KEY,
            product_id CHAR(36) NOT NULL,
            user_id CHAR(36) NOT NULL,
            text TEXT NOT NULL,
            timestamp DATETIME NOT NULL,
            FOREIGN KEY (product_id) REFERENCES products(product_id),
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        );
        '''
        self._create_table(create_table_sql)

    def create_comment(self, product_id, user_id, text):
        """
        Creates a new comment in the database associated with a specific product and user.
        
        Parameters:
            product_id (str): The ID of the product the comment is associated with.
            user_id (str): The ID of the user making the comment.
            text (str): The text of the comment.

        Returns:
            comment_id (str): The ID of the newly created comment.
        """
        # Validate comment
        if not text.strip():
            raise ValueError("Comment text cannot be blank.")
        if contains_banned_words(text):
            raise ValueError("Comment contains inappropriate language.")
        
        # Create the comment
        comment_id = str(uuid.uuid4())
        timestamp = self._get_current_timestamp()
        
        conn = mysql.connector.connect(**self.db_config)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO comments (comment_id, product_id, user_id, text, timestamp) VALUES (%s, %s, %s, %s, %s)',
                       (comment_id, product_id, user_id, text, timestamp))
        conn.commit()
        cursor.close()
        conn.close()

        return comment_id

    def get_comment(self, comment_id):
        """
        Retrieves a comment by its ID from the database.

        Parameters:
            comment_id (str): The ID of the comment.

        Returns:
            comment (dict): A dictionary with the comment details, or None if not found.
        """
        conn = mysql.connector.connect(**self.db_config)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM comments WHERE comment_id = %s', (comment_id,))
        comment = cursor.fetchone()
        cursor.close()
        conn.close()

        if comment:
            return {
                'comment_id': comment[0], 
                'product_id': comment[1],
                'user_id': comment[2], 
                'text': comment[3], 
                'timestamp': comment[4]
            }
        return None

    def get_comments_by_product(self, product_id):
        """
        Retrieves all comments associated with a specific product.

        Parameters:
            product_id (str): The ID of the product.

        Returns:
            comments (list): A list of dictionaries, each containing the details of a comment.
        """
        conn = mysql.connector.connect(**self.db_config)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM comments WHERE product_id = %s', (product_id,))
        comments = cursor.fetchall()
        cursor.close()
        conn.close()

        comment_list = []
        for comment in comments:
            comment_list.append({
                'comment_id': comment[0],
                'product_id': comment[1],
                'user_id': comment[2],
                'text': comment[3],
                'timestamp': comment[4]
            })

        return comment_list

    def delete_comment(self, comment_id):
        """
        Deletes a comment from the database by its ID.

        Parameters:
            comment_id (str): The ID of the comment to delete.

        Returns:
            None
        """
        conn = mysql.connector.connect(**self.db_config)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM comments WHERE comment_id = %s', (comment_id,))
        conn.commit()
        cursor.close()
        conn.close()
    
    def _get_current_timestamp(self):
        """
        Gets the current timestamp in the format 'YYYY-MM-DD HH:MM:SS'.
        
        Returns:
            str: The current timestamp.
        """
        from datetime import datetime
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
