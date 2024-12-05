"""
Module for unit testing the FlaskAPI class.

This module provides a suite of unit tests for the FlaskAPI class using the unittest framework. 
It verifies the functionality of CRUD operations and API endpoints, ensuring proper interactions 
with a mocked database table.

Author: Isabela Yabe
Last Modified: 19/11/2024
Status: Complete

Dependencies:
    - unittest
    - unittest.mock
    - os
    - sys
    - custom_logger
    - flask_api
    - database_manager
"""

import unittest
from unittest.mock import patch, MagicMock
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), 'src')))
from custom_logger import setup_logger
from flask_api import FlaskAPI
from database_manager import DatabaseManager, Config

logger = setup_logger()

class TestFlaskAPI(unittest.TestCase):
    """
    A test suite for the FlaskAPI class.
    """
    def setUp(self):
        """
        Sets up the test environment before each test case.
        Initializes a mock database table and configures FlaskAPI with it.
        """
        logger.info("SetUp module to test")        
        self.mock_db_table = MagicMock()
        self.mock_db_table.table_name = "test_table"
        self.mock_db_table.columns = ["id", "col1", "col2"]
        self.mock_db_table.column_id = "id"

        self.api = FlaskAPI(self.mock_db_table)
        self.app = self.api.app
        self.app.testing = True
        self.client = self.app.test_client()

    @patch("flask_api.tuple_to_dict")
    def test_get_record_api(self, mock_tuple_to_dict):
        """
        Tests the GET endpoint for retrieving a record by ID.
        Ensures the correct response and interaction with the database.
        """
        record_id = "1"
        mock_record = (record_id, "col_1", "col_2")
        self.mock_db_table.get_by_id.return_value = mock_record

        expected_dict = {"id": record_id, "col1": "col_1", "col2": "col_2"}
        mock_tuple_to_dict.return_value = expected_dict

        response = self.client.get(f"/api/{self.mock_db_table.table_name}/{record_id}")

        self.mock_db_table.get_by_id.assert_called_once_with(record_id)        
        mock_tuple_to_dict.assert_called_once_with(mock_record, self.mock_db_table.columns)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, expected_dict)
        logger.info("Test get api by id: OK!!! ---------------------------> TEST 1 OK!!!")

    def test_get_record_api_not_found(self): 
        """
        Tests the GET endpoint when the requested record does not exist.
        """
        record_id = "1"
        mock_record = None
        self.mock_db_table.get_by_id.return_value = mock_record

        response = self.client.get(f"/api/{self.mock_db_table.table_name}/{record_id}")
        
        self.mock_db_table.get_by_id.assert_called_once_with(record_id)        

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, {"error": "Record not found"}) 
        logger.info("Test get api by id not found: OK!!! ---------------------------> TEST 2 OK!!!")
    
    @patch("flask_api.tuple_to_dict")
    def test_create_record_api(self, mock_tuple_to_dict):
        """
        Tests the POST endpoint for creating a new record.
        Ensures the correct data is passed to the database and proper response is returned.
        """
        insert_data = ("value_1", "value_2")
        self.mock_db_table.insert_row.return_value = "id"

        expected_dict = {"col1": "value_1", "col2": "value_2"}
        mock_tuple_to_dict.return_value = expected_dict

        response = self.client.post("/api/test_table", json=insert_data)

        mock_tuple_to_dict.assert_called_once_with(insert_data, self.
        mock_db_table.columns.remove(self.mock_db_table.column_id))
        self.mock_db_table.insert_row.assert_called_once_with(expected_dict)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json, {"message": "Record created"})
        logger.info("Test create record api: OK!!! ---------------------------> TEST 3 OK!!!")        
    
    @patch("flask_api.tuple_to_dict")
    def test_create_record_api_exception(self, mock_tuple_to_dict):
        """
        Tests the POST endpoint for handling exceptions during record creation.
        """
        insert_data = ("value_1", "value_2")
        self.mock_db_table.insert_row.return_value = "id"

        expected_dict = {"col1": "value_1", "col2": "value_2"}
        self.mock_db_table.insert_row.side_effect = Exception("Insert failed")

        mock_tuple_to_dict.return_value = expected_dict

        response = self.client.post("/api/test_table", json=insert_data)

        mock_tuple_to_dict.assert_called_once_with(insert_data, self.
        mock_db_table.columns.remove(self.mock_db_table.column_id))
        self.mock_db_table.insert_row.assert_called_once_with(expected_dict)
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {"error": "Insert failed"})
        logger.info("Test create record api exception: OK!!! ---------------------------> TEST 4 OK!!!")  
        
    def test_update_record_api(self):
        """
        Tests the PUT endpoint for updating an existing record.
        """
        insert_data = {"col2": "value_2"}

        self.mock_db_table.update_row.return_value = None
        
        response = self.client.put("/api/test_table/id", json=insert_data)

        self.mock_db_table.update_row.assert_called_once_with("id", col2="value_2")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"message": "Record update"})
        logger.info("Test update record api: OK!!! ---------------------------> TEST 5 OK!!!") 
    
    
    def test_update_record_api_exception(self):
        """
        Tests the PUT endpoint for handling exceptions during record updates.
        """
        insert_data = {"col2": "value_2"}

        self.mock_db_table.update_row.side_effect = Exception("Exception! Something wrong happened")
        
        response = self.client.put("/api/test_table/id", json=insert_data)

        self.mock_db_table.update_row.assert_called_once_with("id", col2="value_2")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {"error": "Exception! Something wrong happened"})
        logger.info("Test update record api exception: OK!!! ---------------------------> TEST 6 OK!!!")
    
    def test_delete_record_api(self):
        """
        Tests the DELETE endpoint for removing a record by ID.
        """
        self.mock_db_table.delete_row.return_value = None
    
        response = self.client.delete("/api/test_table/id")

        self.mock_db_table.delete_row.assert_called_once_with("id")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"message": "Record deletes"})
        logger.info("Test delete record api: OK!!! ---------------------------> TEST 7 OK!!!")
    
    def test_delete_record_api_exception(self):
        """
        Tests the DELETE endpoint for handling exceptions during record deletion.
        """
        self.mock_db_table.delete_row.side_effect = Exception("Exception! Something wrong hapened!")

        response = self.client.delete("/api/test_table/id")

        self.mock_db_table.delete_row.assert_called_once_with("id")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {"error": "Exception! Something wrong hapened!"})
        logger.info("Test delete record api exception: OK!!! ---------------------------> TEST 8 OK!!!")

    @patch.object(FlaskAPI, 'run')
    def test_run(self, mock_run):
        """
        Tests the run method of the FlaskAPI class to ensure proper invocation.
        """
        self.api.run(debug=True)

        mock_run.assert_called_once_with(debug=True)
    logger.info("Test run: OK!!! ---------------------------> TEST 9 OK!!!")
    
    def test_search_record_api_no_results(self):
        """
        Tests the GET endpoint for searching records when no results are found.
        """
        query_params = {"col1": "nonexistent_value"}
        self.mock_db_table.search_record.return_value = []

        response = self.client.get(f"/api/{self.mock_db_table.table_name}/search", query_string=query_params)

        self.mock_db_table.search_record.assert_called_once_with(**query_params)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, {"error": "No records found"})
        logger.info("Test search record api no results: OK!!! ---------------------------> TEST 10 OK!!!")

    def test_search_record_api_exception(self):
        """
        Tests the GET endpoint for searching records when an exception occurs.
        """
        query_params = {"col1": "value_1"}
        self.mock_db_table.search_record.side_effect = Exception("Search failed")

        response = self.client.get(f"/api/{self.mock_db_table.table_name}/search", query_string=query_params)

        self.mock_db_table.search_record.assert_called_once_with(**query_params)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {"error": "Search failed"})
        logger.info("Test search record api exception: OK!!! ---------------------------> TEST 11 OK!!!")

if __name__ == "__main__":
    unittest.main()