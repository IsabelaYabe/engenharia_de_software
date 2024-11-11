"""
Module for unit testing the UserProfile class.

This module provides unit tests for the `UserProfile` class, which is responsible for managing
CRUD operations on a user profile database table.

Author: Isabela Yabe
Last Modified: 10/11/2024
Status: Complete

Dependencies:
    - unittest
    - unittest.mock
    - uuid
    - os
    - sys
    - UserProfile
    - mysql.connector
"""

import unittest
from unittest.mock import patch, MagicMock
import uuid
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), 'src')))
from profiles.user_profile import UserProfile


class TestUserProfile(unittest.TestCase):
    """
    TestUserProfile class.

    This class contains unit tests for the `UserProfile` class, verifying that the CRUD methods
    function as expected in handling user profile data.

    Methods:
        - setUp: Initializes a UserProfile instance for testing.
        - test_create_table: Tests table creation to ensure it is called correctly.
        - test_insert_row: Tests inserting a new user, checking that the row insertion occurs as expected.
        - test_update_row: Tests updating an existing user's details and verifies the updated data.
        - test_delete_row: Tests the deletion of a user by ID.
        - test_get_by_id: Tests retrieving a user by their ID and checks if the returned data is correct.
    """
    @patch("mysql.connector.connect") 
    def setUp(self, mock_connect):
        """
        Sets up a UserProfile instance for testing by mocking the MySQL connection.
        
        Args:
            mock_connect: Mock object to simulate the MySQL connection.
        """
        self.user_profile = UserProfile(
            host="localhost",
            user="root",
            password="password",
            database="test_db"
        )

    @patch("profiles.user_profile.UserProfile._create_table_")
    def test_create_table(self, mock_create_table):
        """
        Tests that the _create_table method correctly triggers the table creation.
        
        Args:
            mock_create_table: Mock object to simulate the table creation.
        """
        self.user_profile._create_table()
        mock_create_table.assert_called_once()
    
    @patch("uuid.uuid4")
    @patch("profiles.user_profile.UserProfile._insert_row")
    def test_insert_row(self, mock_insert_row, mock_uuid):  
        """
        Tests inserting a new user into the `users` table.

        Args:
            mock_insert_row: Mock object to simulate row insertion.
            mock_uuid: Mock object to generate a consistent UUID for testing.
        """  
        mock_uuid.return_value = uuid.UUID("12345678-1234-5678-1234-567812345678")

        result = self.user_profile.insert_row(
            username="testuser",
            email="testuser@example.com",
            password="hashed_password",
            first_name="Test",
            last_name="User",
            birthdate="2000-01-01",
            phone_number="1234567890",
            address="123 Test Street"
        )
        mock_insert_row.assert_called_once_with(
            id="12345678-1234-5678-1234-567812345678",
            username="testuser",
            email="testuser@example.com",
            password="hashed_password",
            first_name="Test",
            last_name="User",
            birthdate="2000-01-01",
            phone_number="1234567890",
            address="123 Test Street"
        )
        self.assertEqual(result, "12345678-1234-5678-1234-567812345678")

    @patch("profiles.user_profile.UserProfile.get_by_id")
    @patch("profiles.user_profile.UserProfile._update_row")
    def test_update_row(self, mock_update_row, mock_get_by_id):
        """
        Tests updating an existing user's details.

        Args:
            mock_update_row: Mock object to simulate row updating.
            mock_get_by_id: Mock object to retrieve user details.
        """
        user_id = "12345678-1234-5678-1234-567812345678"

        self.user_profile.update_row(user_id, username="new_username", email="new_email@example.com")

        mock_update_row.assert_called_once_with(user_id, "id", username="new_username", email="new_email@example.com")
        
    @patch("profiles.user_profile.UserProfile._delete_row")
    def test_delete_row(self, mock_delete_row):
        """
        Tests deleting a user by ID.

        Args:
            mock_delete_row: Mock object to simulate row deletion.
        """
        user_id = str(uuid.uuid4())
        self.user_profile.delete_row(user_id)

        mock_delete_row.assert_called_once_with(user_id, "id")

    @patch("profiles.user_profile.UserProfile._get_by_id")
    def test_get_by_id(self, mock_get_by_id):
        """
        Tests retrieving a user by their ID.

        Args:
            mock_get_by_id: Mock object to simulate retrieval of a user by ID.
        """
        user_id = str(uuid.uuid4())
        mock_get_by_id.return_value = (
            user_id, "testuser", "testuser@example.com", "hashed_password", 
            "Test", "User", "2000-01-01", "1234567890", "123 Test Street"
        )

        result = self.user_profile.get_by_id(user_id)
        expected_result = {
            "id": user_id,
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "hashed_password",
            "first name": "Test",
            "last name": "User",
            "birthdate": "2000-01-01",
            "phone number": "1234567890",
            "address": "123 Test Street"
        }

        mock_get_by_id.assert_called_once_with(user_id, "id")
        self.assertEqual(result, expected_result)

if __name__ == '__main__':
    unittest.main()
