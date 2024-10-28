import uuid
import mysql.connector
import os
import sys
from utils import contains_banned_words
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from database_manager import DatabaseManager
    

class CommentProfile:
    def __init__(self, host, user, password, database):
        self.connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.cursor = self.connection.cursor()

    def __create_table(self):
        """
        Creates the comments table in the MySQL database if it does not already exist.
        The table stores comments along with the product_id and user_id they are associated with.
        """
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS Comments (
            CommentID INT AUTO_INCREMENT PRIMARY KEY,
            Timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            Text TEXT NOT NULL,
            ProductID INT NOT NULL,
            UserID INT NOT NULL,
            PRIMARY KEY (CommentID),
            FOREIGN KEY (ProductID) REFERENCES Products(ProductID),
            FOREIGN KEY (UserID) REFERENCES User(UserID)
        )
    """
        self.create_table(create_table_sql)

    def create_comment(self, product_id, user_id, text):
        """
        Creates a new comment in the database.

        Parameters:
            product_id (int): The ID of the product the comment is associated with.
            user_id (int): The ID of the user who created the comment.
            text (str): The text of the comment.

        Returns:
            comment_id (str): The ID of the newly created comment.
        """
        # if the comment is empty, raise an error
        if not text or not text.strip():
            raise ValueError("Comment cannot be empty.")
        # if the comment contains banned words, raise an error
        if contains_banned_words(text):
            raise ValueError("Comment contains banned words.")

        query = "INSERT INTO Comments (ProductID, UserID, Text, Timestamp) VALUES (%s, %s, %s, %s)"
        self.cursor.execute(query, (product_id, user_id, text, self._get_current_timestamp()))
        self.connection.commit()
        return self.cursor.lastrowid

    def get_comments_by_product(self, product_id):
        """
        Retrieves all comments associated with a product from the database.

        Parameters:
            product_id (int): The ID of the product to retrieve comments for.

        Returns:
            comments (list): A list of dictionaries containing the details of the comments.
        """
        query = "SELECT * FROM Comments WHERE ProductID = %s"
        self.cursor.execute(query, (product_id,))
        comments = self.cursor.fetchall()
        
        # Verifica se o tipo do campo `timestamp` é datetime, e faz a formatação adequadamente
        return [
        {
            'CommentID': comment[0],  # id
            'ProductID': comment[2],  # product_id
            'UserID': comment[3],     # user_id
            'Text': comment[4],        # text
            'Timestamp': comment[1]    # timestamp
        }
        for comment in comments
    ]



    def get_comment(self, comment_id):
        """
        Retrieves a comment from the database by its ID.

        Parameters:
            comment_id (str): The ID of the comment to retrieve.

        Returns:
            comment (dict): A dictionary containing the details of the comment.
        """
        query = "SELECT * FROM Comments WHERE CommentID = %s"
        self.cursor.execute(query, (comment_id,))
        comment = self.cursor.fetchone()
        if comment:
            return {
                'CommentID': comment[0],
                'ProductID': comment[1],
                'UserID': comment[2],
                'Text': comment[3],
                'Timestamp': comment[4]
            }
        else:
            return None
        
    def delete_comment(self, comment_id):
        """
        Deletes a comment from the database by its ID.

        Parameters:
            comment_id (str): The ID of the comment to delete.
        """
        query = "DELETE FROM Comments WHERE CommentID = %s"
        self.cursor.execute(query, (comment_id,))
        self.connection.commit()

    
    def _get_current_timestamp(self):
        """
        Gets the current timestamp in the format 'YYYY-MM-DD HH:MM:SS'.
        
        Returns:
            str: The current timestamp.
        """
        from datetime import datetime
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    def close(self):
        """
        Closes the database connection.
        """
        self.cursor.close()
        self.connection.close()


if __name__ == "__main__":
    db_config = {
        "host": "localhost",
        "user": "root",
        "password": "Alacazumba123*",
        "database": "my_database"
    }
    comment_profile = CommentProfile(**db_config)
    print("CommentProfile class created successfully.")

    # Inserting a comment
    product_id = 3
    user_id = 1
    text = "TEST COMMENT"
    comment_id = comment_profile.create_comment(product_id, user_id, text)
    print(f"Comment created with ID: {comment_id}")

    # Retrieving comments by product
    comments = comment_profile.get_comments_by_product(product_id)
    print("Comments for product_id 1:")
