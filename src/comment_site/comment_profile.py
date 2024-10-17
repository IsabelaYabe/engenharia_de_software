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
            id INT AUTO_INCREMENT PRIMARY KEY,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            product_id INT NOT NULL,
            user_id INT NOT NULL,
            text TEXT NOT NULL,
            FOREIGN KEY (product_id) REFERENCES Products(id),
            FOREIGN KEY (user_id) REFERENCES Users(id)
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
        if not text:
            raise ValueError("Comment cannot be empty.")
        # if the comment contains banned words, raise an error
        if contains_banned_words(text):
            raise ValueError("Comment contains banned words.")

        query = "INSERT INTO comments (product_id, user_id, text, timestamp) VALUES (%s, %s, %s, %s)"
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
        query = "SELECT * FROM comments WHERE product_id = %s"
        self.cursor.execute(query, (product_id,))
        comments = self.cursor.fetchall()
        
        # Verifica se o tipo do campo `timestamp` é datetime, e faz a formatação adequadamente
        return [
        {
            'comment_id': comment[0],  # id
            'product_id': comment[2],  # product_id
            'user_id': comment[3],     # user_id
            'text': comment[4],        # text
            'timestamp': comment[1]    # timestamp
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
        query = "SELECT * FROM comments WHERE comment_id = %s"
        self.cursor.execute(query, (comment_id,))
        comment = self.cursor.fetchone()
        if comment:
            return {
                'comment_id': comment[0],
                'product_id': comment[1],
                'user_id': comment[2],
                'text': comment[3],
                'timestamp': comment[4]
            }
        else:
            return None
        
    def delete_comment(self, comment_id):
        """
        Deletes a comment from the database by its ID.

        Parameters:
            comment_id (str): The ID of the comment to delete.
        """
        query = "DELETE FROM comments WHERE comment_id = %s"
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
