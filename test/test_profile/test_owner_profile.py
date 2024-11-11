"""
Module for unit testing the OwnerProfile class.

This module provides unit tests for the `OwnerProfile` class, which is responsible for managing
CRUD operations on a owner profile database table.

Author: Isabela Yabe
Last Modified: 10/11/2024
Status: Complete

Dependencies:
    - unittest
    - unittest.mock
    - uuid
    - os
    - sys
    - OwnerProfile
    - mysql.connector
"""

import unittest
from unittest.mock import patch, MagicMock
import uuid
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), 'src')))
from profiles.owner_profile import OwnerProfile


class TestOwnerProfile(unittest.TestCase):
    """
    TestOwnerProfile class.

    This class contains unit tests for the `OwnerProfile` class, verifying that the CRUD methods
    function as expected in handling owner profile data.

    Methods:
        - setUp: Initializes a OwnerProfile instance for testing.
        - test_create_table: Tests table creation to ensure it is called correctly.
        - test_insert_row: Tests inserting a new owner, checking that the row insertion occurs as expected.
        - test_update_row: Tests updating an existing owner's details and verifies the updated data.
        - test_delete_row: Tests the deletion of a owner by ID.
        - test_get_by_id: Tests retrieving a owner by their ID and checks if the returned data is correct.
    """
    @patch("mysql.connector.connect") 
    def setUp(self, mock_connect):
        """
        Sets up a OwnerProfile instance for testing by mocking the MySQL connection.
        
        Args:
            mock_connect: Mock object to simulate the MySQL connection.
        """
        self.owner_profile = OwnerProfile(
            host="localhost",
            user="root",
            password="password",
            database="test_db"
        )

    @patch("profiles.owner_profile.OwnerProfile._create_table_")
    def test_create_table(self, mock_create_table):
        """
        Tests that the _create_table method correctly triggers the table creation.
        
        Args:
            mock_create_table: Mock object to simulate the table creation.
        """
        self.owner_profile._create_table()
        mock_create_table.assert_called_once()
    
    @patch("uuid.uuid4")
    @patch("profiles.owner_profile.OwnerProfile._insert_row")
    def test_insert_row(self, mock_insert_row, mock_uuid):  
        """
        Tests inserting a new owner into the `owners` table.

        Args:
            mock_insert_row: Mock object to simulate row insertion.
            mock_uuid: Mock object to generate a consistent UUID for testing.
        """  
        mock_uuid.return_value = uuid.UUID("12345678-1234-5678-1234-567812345678")

        result = self.owner_profile.insert_row(
            ownername="testowner",
            email="testowner@example.com",
            password="hashed_password",
            first_name="Test",
            last_name="Owner",
            birthdate="2000-01-01",
            phone_number="1234567890",
            address="123 Test Street"
        )
        mock_insert_row.assert_called_once_with(
            id="12345678-1234-5678-1234-567812345678",
            ownername="testowner",
            email="testowner@example.com",
            password="hashed_password",
            first_name="Test",
            last_name="Owner",
            birthdate="2000-01-01",
            phone_number="1234567890",
            address="123 Test Street"
        )
        self.assertEqual(result, "12345678-1234-5678-1234-567812345678")

    @patch("profiles.owner_profile.OwnerProfile.get_by_id")
    @patch("profiles.owner_profile.OwnerProfile._update_row")
    def test_update_row(self, mock_update_row, mock_get_by_id):
        """
        Tests updating an existing owner's details.

        Args:
            mock_update_row: Mock object to simulate row updating.
            mock_get_by_id: Mock object to retrieve owner details.
        """
        owner_id = "12345678-1234-5678-1234-567812345678"

        self.owner_profile.update_row(owner_id, ownername="new_ownername", email="new_email@example.com")

        mock_update_row.assert_called_once_with(owner_id, "id", ownername="new_ownername", email="new_email@example.com")
        
    @patch("profiles.owner_profile.OwnerProfile._delete_row")
    def test_delete_row(self, mock_delete_row):
        """
        Tests deleting a owner by ID.

        Args:
            mock_delete_row: Mock object to simulate row deletion.
        """
        owner_id = str(uuid.uuid4())
        self.owner_profile.delete_row(owner_id)

        mock_delete_row.assert_called_once_with(owner_id, "id")

    @patch("profiles.owner_profile.OwnerProfile._get_by_id")
    def test_get_by_id(self, mock_get_by_id):
        """
        Tests retrieving a owner by their ID.

        Args:
            mock_get_by_id: Mock object to simulate retrieval of a owner by ID.
        """
        owner_id = str(uuid.uuid4())
        mock_get_by_id.return_value = (
            owner_id, "testowner", "testowner@example.com", "hashed_password", 
            "Test", "Owner", "2000-01-01", "1234567890", "123 Test Street"
        )

        result = self.owner_profile.get_by_id(owner_id)
        expected_result = {
            "id": owner_id,
            "ownername": "testowner",
            "email": "testowner@example.com",
            "password": "hashed_password",
            "first name": "Test",
            "last name": "Owner",
            "birthdate": "2000-01-01",
            "phone number": "1234567890",
            "address": "123 Test Street"
        }

        mock_get_by_id.assert_called_once_with(owner_id, "id")
        self.assertEqual(result, expected_result)

if __name__ == '__main__':
    unittest.main()
