"""
Module for Testing PasswordHasher Class.

This module provides a suite of unit tests for the `PasswordHasher` class using the `unittest` framework.
It tests various hashing functionalities, input validation, and the behavior of the `hash_password_decorator`.

Author: Isabela Yabe
Last Modified: 07/12/2024
Status: Complete

Dependencies:
    - unittest
    - unittest.mock
    - custom_logger.setup_logger
    - password_hasher.PasswordHasher
    - password_hasher.hash_password_decorator
"""

import unittest
from unittest.mock import patch, MagicMock
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.getcwd(),"src")))
from password_hasher import PasswordHasher, hash_password_decorator
from custom_logger import setup_logger

logger = setup_logger()

class MockClassWithDecorator:
    """
    Mock class to test the hash_password_decorator.
    """
    def __init__(self):
        self.password_hasher = PasswordHasher()

    @hash_password_decorator
    def create_user(self, username, password):
        """
        Mock method to simulate a user creation process.
        """
        return {"username": username, "password": password}


class TestPasswordHasher(unittest.TestCase):
    """
    TestPasswordHasher class.

    This class provides unit tests for the `PasswordHasher` class, focusing on its ability to hash passwords
    and manage its singleton instance.
    """

    def setUp(self):
        """
        Set up the test environment before each test case.
        """
        self.password_hasher = PasswordHasher()
        self.mock_class = MockClassWithDecorator()

    def test_singleton_instance(self):
        """
        Test if PasswordHasher follows the Singleton pattern.
        """
        new_instance = PasswordHasher()
        self.assertIs(self.password_hasher, new_instance, "PasswordHasher does not follow the Singleton pattern.")
        logger.info("Test singleton instance: OK!!! ---------------------------> TEST 1 OK!!!")
    def test_hash_password_success(self):
        """
        Test hashing a valid password.
        """
        password = "mypassword123"
        hashed_password = self.password_hasher.hash_password(password)
        expected_hash = PasswordHasher().hash_password(password)
        self.assertEqual(hashed_password, expected_hash, "The password hash is not as expected.")
        logger.info("Test hash password success: OK!!! ---------------------------> TEST 2 OK!!!")

    def test_hash_password_is_deterministic(self):
        """
        Test if the hash of the same password is consistent.
        """
        password = "mypassword123"
        hash1 = self.password_hasher.hash_password(password)
        hash2 = self.password_hasher.hash_password(password)
        self.assertEqual(hash1, hash2, "Hashing is not deterministic for the same password.")
        logger.info("Test hash password is deterministic: OK!!! ---------------------------> TEST 3 OK!!!")

    def test_hash_password_raises_value_error_for_non_string(self):
        """
        Test if ValueError is raised when the password is not a string.
        """
        with self.assertRaises(ValueError):
            self.password_hasher.hash_password(123456)  
        logger.info("Test hash password raises value error for non string: OK!!! ---------------------------> TEST 4 OK!!!")

    def test_hash_password_is_not_empty(self):
        """
        Test if the hash result is not an empty string.
        """
        password = "mypassword123"
        hashed_password = self.password_hasher.hash_password(password)
        self.assertTrue(len(hashed_password) > 0, "The hash should not be an empty string.")
        logger.info("Test hash password is not empty: OK!!! ---------------------------> TEST 5 OK!!!")

    def test_hash_password_has_correct_length(self):
        """
        Test if the hash result has a length of 64 characters (SHA-256).
        """
        password = "mypassword123"
        hashed_password = self.password_hasher.hash_password(password)
        self.assertEqual(len(hashed_password), 64, "The hash should have a length of 64 characters (SHA-256).")
        logger.info("Test hash password has correct length: OK!!! ---------------------------> TEST 6 OK!!!")

    def test_hash_password_correct_content(self):
        """
        Test if the hash is hexadecimal and not arbitrary text.
        """
        password = "mypassword123"
        hashed_password = self.password_hasher.hash_password(password)
        self.assertTrue(all(c in "0123456789abcdef" for c in hashed_password), "The hash should only contain hexadecimal characters.")
        logger.info("Test hash password correct content: OK!!! ---------------------------> TEST 7 OK!!!")

    def test_hash_password_decorator_hashes_password(self):
        """
        Test if the hash_password_decorator correctly hashes the password.
        """
        username = "isabela"
        password = "mypassword123"
        result = self.mock_class.create_user(username=username, password=password)
        expected_hash = self.password_hasher.hash_password(password)
        self.assertEqual(result["password"], expected_hash, "The decorator did not hash the password correctly.")
        logger.info("Test hash password decorator hashes password: OK!!! ---------------------------> TEST 8 OK!!!")

    def test_decorator_does_not_alter_username(self):
        """
        Test if the decorator does not alter the username.
        """
        username = "isabela"
        password = "mypassword123"
        result = self.mock_class.create_user(username=username, password=password)
        self.assertEqual(result["username"], username, "The username should not be altered by the decorator.")
        logger.info("Test decorator does not alter username: OK!!! ---------------------------> TEST 9 OK!!!")

    def test_decorator_does_not_raise_error_if_password_not_in_kwargs(self):
        """
        Test if the decorator does not raise an error when 'password' is not in kwargs.
        """
        result = self.mock_class.create_user("isabela", "mypassword123")
        self.assertIn("username", result, "The decorator should not raise an error if 'password' is not in kwargs.")
        logger.info("Test decorator does not raise error if password not in kwargs: OK!!! ---------------------------> TEST 10 OK!!!")

    def test_decorator_works_with_no_kwargs(self):
        """
        Test if the decorator works correctly when kwargs are not provided.
        """
        result = self.mock_class.create_user("isabela", "mypassword123")
        self.assertIn("password", result, "The decorator should not fail if kwargs are not present.")
        logger.info("Test decorator works with no kwargs: OK!!! ---------------------------> TEST 11 OK!!!")

    def test_decorator_does_not_raise_error_if_password_not_in_kwargs(self):
        """
        Test if the decorator does not raise an error when "password" is not in kwargs.
        """
        result = self.mock_class.create_user("isabela", "mypassword123")
        self.assertIn("username", result, "The decorator should not raise an error if 'password' is not in kwargs.")
        logger.info("Test decorator does not raise error if password not in kwargs: OK!!! ---------------------------> TEST 12 OK!!!")

    def test_log_password_hashing(self):
        """
        Test if the logger logs the correct message during password hashing.
        """
        with patch("password_hasher.logger.info") as mock_logger_info:
            password = "mypassword123"
            self.password_hasher.hash_password(password)
            mock_logger_info.assert_any_call("Hashing password using SHA-256.")
            logger.info("Test log password hashing: OK!!! ---------------------------> TEST 13 OK!!!")

    def test_log_error_for_non_string_password(self):
        """
        Test if the logger logs an error message when a non-string password is provided.
        """
        with patch("password_hasher.logger.error") as mock_logger_error:
            with self.assertRaises(ValueError):
                self.password_hasher.hash_password(123456)
            mock_logger_error.assert_any_call("Invalid password type. Expected a string.")
            logger.info("Test log error for non string password: OK!!! ---------------------------> TEST 14 OK!!!")

    def test_decorator_logs_password_hashing(self):
        """
        Test if the decorator logs the password hashing.
        """
        with patch("password_hasher.logger.info") as mock_logger_info:
            self.mock_class.create_user(username="isabela", password="mypassword123")
            mock_logger_info.assert_any_call("Hashing password before calling the original function.")
            logger.info("Test decorator logs password hashing: OK!!! ---------------------------> TEST 15 OK!!!")

if __name__ == "__main__":
    unittest.main()
