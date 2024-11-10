"""
    Module for unit testing the VMProfile class.

    This module provides unit tests for the `VMProfile` class, which is responsible for managing
    CRUD operations on a vending machine profile database table.

    Author: Isabela Yabe
    Last Modified: 10/11/2024
    Status: Complete

    Dependencies:
        - unittest
        - unittest.mock
        - uuid
        - os
        - sys
        - VMProfile
        - mysql.connector
"""

import unittest
from unittest.mock import patch, MagicMock
import uuid
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), 'src')))
from vending_machine_profile import VMProfile


class TestVMProfile(unittest.TestCase):
    """
    TestVMProfile class.

    This class contains unit tests for the `VMProfile` class, verifying that the CRUD methods
    function as expected in handling vending machine profile data.

    Methods:
        - setUp: Initializes a VMProfile instance for testing.
        - test_create_table: Tests table creation to ensure it is called correctly.
        - test_insert_row: Tests inserting a new vending machine, checking that the row insertion occurs as expected.
        - test_update_row: Tests updating an existing vending machine and verifies the updated data.
        - test_delete_row: Tests the deletion of a vending machine by ID.
        - test_get_by_id: Tests retrieving a vending machine by its ID and checks if the returned data is correct.
    """
    @patch("mysql.connector.connect") 
    def setUp(self, mock_connect):
        """
        Sets up a VMProfile instance for testing by mocking the MySQL connection.
        
        Args:
            mock_connect: Mock object to simulate the MySQL connection.
        """
        self.vending_machine_profile = VMProfile(
            host = "localhost",
            user = "root",
            password = "password",
            database="test_db"
        )

    @patch("vending_machine_profile.VMProfile._create_table_")
    def test_create_table(self, mock_create_table):
        """
        Tests that the _create_table method correctly triggers the table creation.
        
        Args:
            mock_create_table: Mock object to simulate the table creation.
        """
        self.vending_machine_profile._create_table()
        mock_create_table.assert_called_once()
    
    @patch("uuid.uuid4")
    @patch("vending_machine_profile.VMProfile._insert_row")
    def test_insert_row(self, mock_insert_row, mock_uuid):  
        """
        Tests inserting a new vending machine into the `vending machines` table.

        Args:
            mock_insert_row: Mock object to simulate row insertion.
            mock_uuid: Mock object to generate a consistent UUID for testing.
        """  
        mock_uuid.return_value = uuid.UUID("12345678-1234-5678-1234-567812345678")

        result = self.vending_machine_profile.insert_row("machine name", "EMAp", "Defective")
        mock_insert_row.assert_called_once_with(
            id = "12345678-1234-5678-1234-567812345678",
            name = "machine name",
            location = "EMAp",
            status = "Defective"
        )
        self.assertEqual(result, "12345678-1234-5678-1234-567812345678")

    @patch("vending_machine_profile.VMProfile.get_by_id")
    @patch("vending_machine_profile.VMProfile._update_row")
    def test_update_row(self, mock_update_row, mock_get_by_id):
        """
        Tests updating an existing vending machine's details.

        Args:
            mock_update_row: Mock object to simulate row updating.
            mock_get_by_id: Mock object to retrieve vending machine details.
        """
        vending_machine_id = "12345678-1234-5678-1234-567812345678"

        self.vending_machine_profile.update_row(vending_machine_id, status="In operation")

        mock_update_row.assert_called_once_with(vending_machine_id, "id", status="In operation")

    @patch("vending_machine_profile.VMProfile._delete_row")
    def test_delete_row(self, mock_delete_row):
        """
        Tests deleting a vending machine by ID.

        Args:
            mock_delete_row: Mock object to simulate row deletion.
        """
        vending_machine_id = str(uuid.uuid4())
        self.vending_machine_profile.delete_row(vending_machine_id)

        mock_delete_row.assert_called_once_with(vending_machine_id, "id")

    @patch("vending_machine_profile.VMProfile._get_by_id")
    def test_get_by_id(self, mock_get_by_id):
        """
        Tests retrieving a vending machine by its ID.

        Args:
            mock_get_by_id: Mock object to simulate retrieval of a vending machine by ID.
        """
        vending_machine_id = str(uuid.uuid4())
        mock_get_by_id.return_value = (vending_machine_id, "machine name", "EMAp", "Defective")

        result = self.vending_machine_profile.get_by_id(vending_machine_id)
        expected_result = {
            "id": vending_machine_id,
            "name": "machine name",
            "location": "EMAp",
            "status": "Defective"
            }

        mock_get_by_id.assert_called_once_with(vending_machine_id, "id")
        self.assertEqual(result, expected_result)

if __name__ == '__main__':
    unittest.main()