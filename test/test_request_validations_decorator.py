"""
Module for unit testing the request_validations decorator.

This module provides unit tests for the `request_validations` decorator. The tests check if the decorator correctly applies validation strategies (e.g., `BannedWordsStrategy` and `SQLInjectionStrategy`) to incoming requests. The module uses Flask's test client to simulate HTTP requests and ensures the decorator behaves as expected.

Author: Isabela Yabe
Last Modified: 09/11/2024
Status: Complete

Dependencies:
    - unittest
    - unittest.mock
    - flask
    - os
    - sys
    - decorators.request_validations
    - banned_words_strategy.BannedWordsStrategy
    - sql_injection_strategy.SQLInjectionStrategy
"""

import unittest
from unittest.mock import MagicMock, patch
from flask import Flask, jsonify, request

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), 'src')))
from decorators import request_validations
from banned_words_strategy import BannedWordsStrategy
from sql_injection_strategy import SQLInjectionStrategy

class TestRequestValidationsDecorator(unittest.TestCase):
    def setUp(self):
        """
        Sets up the Flask app and test endpoint with the request_validations decorator.
        """
        self.app = Flask(__name__)
        self.banned_words_strategy = BannedWordsStrategy()
        self.sql_injection_strategy = SQLInjectionStrategy()

        @self.app.route("/test", methods=["POST", "PUT"])
        @request_validations([self.banned_words_strategy, self.sql_injection_strategy], "POST", "PUT")
        def test_route():
            return jsonify({"message": "Request passed validation"}), 200

        self.client = self.app.test_client()

    @patch.object(BannedWordsStrategy, "validate", return_value=None)
    @patch.object(SQLInjectionStrategy, "validate", return_value=None)
    def test_request_with_valid_data(self, mock_sql_validate, mock_banned_words_validate):
        """
        Tests that a request with valid data passes all validations.
        """
        data = {"text": "This is a valid request"}

        response = self.client.post("/test", json=data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"message": "Request passed validation"})

    @patch.object(BannedWordsStrategy, "validate", return_value="Request contains banned words.")
    def test_request_with_banned_words(self, mock_banned_words_validate):
        """
        Tests that a request containing banned words is blocked.
        """
        data = {"text": "This is a badword"}

        response = self.client.post("/test", json=data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {"error": "Request contains banned words."})

    @patch.object(SQLInjectionStrategy, "validate", return_value="Request contains potentially dangerous SQL keywords.")
    def test_request_with_sql_injection(self, mock_sql_injection):
        """
        Tests that a request containing SQL injection patterns is blocked.
        """
        data = {"test": "DROP TABLE users;"}

        response = self.client.post("/test", json=data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {"error": "Request contains potentially dangerous SQL keywords."})

if __name__ == "__main__":
    unittest.main()