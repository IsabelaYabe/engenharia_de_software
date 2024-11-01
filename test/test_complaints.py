'''
    This Module contains the test cases for the Complaint class in the complaints module.

    Author: Lavinia Dias
'''

import unittest
from unittest.mock import patch, MagicMock
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../src/profiles'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))
from complaint_profile import Complaint  
from utils import contains_banned_words  

class TestComplaint(unittest.TestCase):
    """
    Test cases for the Complaint class.

    Methods:
    - setUp: Configures the mock connection and cursor.
    - test_create_complaint: Tests the creation of a complaint.
    - test_create_complaint_with_banned_words: Tests the creation of a complaint with banned words.
    - test_create_complaint_empty_text: Tests the creation of a complaint with empty text.

    - test_get_complaints_by_vending_machine: Tests the retrieval of complaints by vending machine.
    - test_delete_complaint: Tests the deletion of a complaint.
    - tearDown: Destroys the complaint object.
    """
    @patch("complaint_profile.mysql.connector.connect")
    def setUp(self, mock_connect):
        """
        Configures the mock connection and cursor.

        Parameters:
            mock_connect (MagicMock): The mock connection 

        Returns:
            None
        
        """
        # Configure mock connection and cursor
        self.mock_connection = MagicMock()
        self.mock_cursor = MagicMock()
        mock_connect.return_value = self.mock_connection
        self.mock_connection.cursor.return_value = self.mock_cursor
        
        # Instantiate the Complaint class
        self.complaint = Complaint("host", "user", "password", "database")
    
    def test_create_complaint(self):
        """
        Tests the creation of a complaint.
        
        Parameters:
            None
            
        Returns:    
            None
        """
        # Test to create a complaint
        self.mock_cursor.lastrowid = 1  
        complaint_id = self.complaint.create_complaint(1, "user123", "This machine is not working properly.")
        
        # Verify that the complaint was created
        self.mock_cursor.execute.assert_called_once()
        self.mock_connection.commit.assert_called_once()
        self.assertEqual(complaint_id, 1)
    
    @patch("complaint_profile.contains_banned_words", return_value=True)
    def test_create_complaint_with_banned_words(self, mock_banned_words):
        """
        Tests the creation of a complaint with banned words.

        Parameters:
            mock_banned_words (MagicMock): The mock banned words function

        Returns:
            None
        """

        # Test to create a complaint with banned words
        with self.assertRaises(ValueError):
            self.complaint.create_complaint(1, "user123", "This text contains banned words.")
    
    def test_create_complaint_empty_text(self):
        """
        Tests the creation of a complaint with empty text.

        Parameters:
            None

        Returns:
            None
        """
        # Test to create a complaint with empty text
        with self.assertRaises(ValueError):
            self.complaint.create_complaint(1, "user123", "")
    
    def test_get_complaints_by_vending_machine(self):
        """
        Tests the retrieval of complaints by vending machine.

        Parameters:
            None

        Returns:
            None
        """
        # Mock the fetchall method to return a complaint
        self.mock_cursor.fetchall.return_value = [
            (1, "2023-10-10 12:00:00", 1, "Complaint text", "user123")
        ]
        complaints = self.complaint.get_complaints_by_vending_machine(1)
        
        self.mock_cursor.execute.assert_called_once_with("SELECT * FROM Complaints WHERE vending_machine_id = %s", (1,))
        self.assertEqual(len(complaints), 1)
        self.assertEqual(complaints[0]['complaint_id'], 1)
    
    def test_delete_complaint(self):
        """
        Tests the deletion of a complaint.

        Parameters:
            None

        Returns:
            None
        """
        # Test to delete a complaint by ID
        self.complaint.delete_complaint(1)
        
        self.mock_cursor.execute.assert_called_once_with("DELETE FROM Complaints WHERE id = %s", (1,))
        self.mock_connection.commit.assert_called_once()

    def tearDown(self):
        """
        Destroys the complaint object.

        Parameters:
            None

        Returns:    
            None
        """
        self.complaint = None

if __name__ == "__main__":
    unittest.main()
