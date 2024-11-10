"""
    Module for unit testing the CommentProfile class.

    This module provides unit tests for the `CommentProfile` class, which is responsible for managing
    CRUD operations on a comment profile database table.

    Author: Isabela Yabe
    Last Modified: 10/11/2024
    Status: Complete

    Dependencies:
        - unittest
        - unittest.mock
        - uuid
        - os
        - sys
        - CommentProfile
        - mysql.connector
"""

import unittest
from unittest.mock import patch, MagicMock
import uuid
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), 'src')))
from comment_profile import CommentProfile


class TestCommentProfile(unittest.TestCase):
    """
    TestCommentProfile class.

    This class contains unit tests for the `CommentProfile` class, verifying that the CRUD methods
    function as expected in handling comment profile data.

    Methods:
        - setUp: Initializes a CommentProfile instance for testing.
        - test_create_table: Tests table creation to ensure it is called correctly.
        - test_insert_row: Tests inserting a new comment, checking that the row insertion occurs as expected.
        - test_update_row: Tests updating an existing comment and verifies the updated data.
        - test_delete_row: Tests the deletion of a comment by ID.
        - test_get_by_id: Tests retrieving a comment by its ID and checks if the returned data is correct.
    """
    @patch("mysql.connector.connect") 
    def setUp(self, mock_connect):
        """
        Sets up a CommentProfile instance for testing by mocking the MySQL connection.
        
        Args:
            mock_connect: Mock object to simulate the MySQL connection.
        """
        self.comment_profile = CommentProfile(
            host = "localhost",
            user = "root",
            password = "password",
            database="test_db"
        )

    @patch("comment_profile.CommentProfile._create_table_")
    def test_create_table(self, mock_create_table):
        """
        Tests that the _create_table method correctly triggers the table creation.
        
        Args:
            mock_create_table: Mock object to simulate the table creation.
        """
        self.comment_profile._create_table()
        mock_create_table.assert_called_once()
    
    @patch("uuid.uuid4")
    @patch("comment_profile.CommentProfile._insert_row")
    def test_insert_row(self, mock_insert_row, mock_uuid):  
        """
        Tests inserting a new comment into the `comments` table.

        Args:
            mock_insert_row: Mock object to simulate row insertion.
            mock_uuid: Mock object to generate a consistent UUID for testing.
        """  
        mock_uuid.return_value = uuid.UUID("12345678-1234-5678-1234-567812345678")

        result = self.comment_profile.insert_row("Test Comment")
        mock_insert_row.assert_called_once_with(
            id = "12345678-1234-5678-1234-567812345678",
            text = "Test Comment"
        )
        self.assertEqual(result, "12345678-1234-5678-1234-567812345678")

    @patch("comment_profile.CommentProfile.get_by_id")
    @patch("comment_profile.CommentProfile._update_row")
    def test_update_row(self, mock_update_row, mock_get_by_id):
        """
        Tests updating an existing comment's details.

        Args:
            mock_update_row: Mock object to simulate row updating.
            mock_get_by_id: Mock object to retrieve comment details.
        """
        comment_id = "12345678-1234-5678-1234-567812345678"

        self.comment_profile.update_row(comment_id, text="New Comment")

        mock_update_row.assert_called_once_with(comment_id, "id", text="New Comment")

    @patch("comment_profile.CommentProfile._delete_row")
    def test_delete_row(self, mock_delete_row):
        """
        Tests deleting a comment by ID.

        Args:
            mock_delete_row: Mock object to simulate row deletion.
        """
        comment_id = str(uuid.uuid4())
        self.comment_profile.delete_row(comment_id)

        mock_delete_row.assert_called_once_with(comment_id, "id")

    @patch("comment_profile.CommentProfile._get_by_id")
    def test_get_by_id(self, mock_get_by_id):
        """
        Tests retrieving a comment by its ID.

        Args:
            mock_get_by_id: Mock object to simulate retrieval of a comment by ID.
        """
        comment_id = str(uuid.uuid4())
        mock_get_by_id.return_value = (comment_id, "Test Comment", "2024-11-09 18:02:39,885")

        result = self.comment_profile.get_by_id(comment_id)
        expected_result = {
            "id": comment_id, 
            "text": "Test Comment",
            "timestamp": "2024-11-09 18:02:39,885"
            }

        mock_get_by_id.assert_called_once_with(comment_id, "id")
        self.assertEqual(result, expected_result)

if __name__ == '__main__':
    unittest.main()