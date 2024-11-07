"""
Module for unit testing the FlaskAPI class.

This module provides unit tests for the FlaskAPI class, which connects a Flask application 
to a database table through RESTful API endpoints. The tests simulate HTTP requests to verify
that each API endpoint functions correctly, handles data accurately, and manages errors as expected.

Author: Isabela Yabe

Last Modified: 06/11/2024

Dependencies:
    - unittest
    - unittest.mock
    - os
    - sys
    - custom_logger
    - flask_api
    - database_manager
    - test_db_manager_concrete
"""

import unittest
from unittest.mock import patch, MagicMock
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), 'src')))
from custom_logger import setup_logger
from flask_api import FlaskAPI
from database_manager import DatabaseManager
from test_db_manager_concrete import TestDatabaseManagerConcrete

logger = setup_logger()

class TestFlaskAPI(unittest.TestCase):
    def setUp(self):
        logger.info("SetUp module to test")
        self.mock_db_table = TestDatabaseManagerConcrete(
            host="localhost",
            user="root",
            password="password",
            database="test_db",
            table_name="test_table"
        )
        
        self.mock_db_table._create_table = MagicMock()
        self.mock_db_table.insert_row = MagicMock()
        self.mock_db_table.update_row = MagicMock()
        self.mock_db_table.delete_row = MagicMock()
        self.mock_db_table.get_by_id = MagicMock()

        self.api = FlaskAPI(self.mock_db_table)
        self.app = self.api._app
        self.app.testing = True
        self.client = self.app.test_client()


    def test_get_record_api(self): 
        """
        Test get_record_api method when a record is found.
        """
        self.mock_db_table.get_by_id.return_value = {"id": "instance_id", "name": "instance_name"}

        response = self.client.get("/api/test_table/instance_id")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"id": "instance_id", "name": "instance_name"})
    
    def test_get_record_api_not_found(self):
        """
        Test get_record_api method when a record isn't found.
        """
        self.mock_db_table.get_by_id.return_value = None

        response = self.client.get("/api/test_table/instance_id")

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, {"error": "Record not found"})

    def test_create_record_api(self):
        """
        Test create_record_api method. 
        """
        self.mock_db_table.insert_row.return_value = "id"

        data = ("id", "name_1", 11.99)

        response = self.client.post("/api/test_table", json=data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json, {"message": "Record created"})
        self.mock_db_table.insert_row.assert_called_once_with("id", "name_1", 11.99)

    def test_create_record_api_exception(self):
        """
        Test create_record_api method exception. 
        """
        self.mock_db_table.insert_row.side_effect = Exception("Exception! Something wrong happened")

        data = ("name_1", 11.99)

        response = self.client.post("/api/test_table", json=data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {"error": "Exception! Something wrong happened"})

    def test_update_record_api(self):
        """
        Test update_record_api method.
        """
        self.mock_db_table.update_row.return_value = None

        data = {"name": "name_0", "price": 11.99}

        response = self.client.put("/api/test_table/instance_id", json=data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"message": "Record update"})
        self.mock_db_table.update_row.assert_called_once_with("instance_id", name="name_0", price=11.99)
    def test_update_record_api_exception(self):
        """
        Test update_record_api method exception.
        """
        self.mock_db_table.update_row.side_effect = Exception("Exception! Something wrong happened")
        
        data = {"name": "name_0", "price": 11.99}
    
        response = self.client.put("/api/test_table/instance_id", json=data)
    
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {"error": "Exception! Something wrong happened"})

    def test_delete_record_api(self):
        """
        Test delete_record_api method. 
        """
        self.mock_db_table.delete_row.return_value = None
    
        response = self.client.delete("/api/test_table/instace_id")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"message": "Record deletes"})

    def test_delete_record_api_exception(self):
        """
        Test delete_record_api methos exception.
        """

        self.mock_db_table.delete_row.side_effect = Exception("Exception! Something wrong hapened!")

        response = self.client.delete("/api/test_table/instance_id")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {"error": "Exception! Something wrong hapened!"})

    @patch.object(FlaskAPI, 'run')
    def test_run(self, mock_run):
        """
        Test the run method.
        """
        self.api.run(debug=True)

        mock_run.assert_called_once_with(debug=True)

if __name__ == "__main__":
    unittest.main()