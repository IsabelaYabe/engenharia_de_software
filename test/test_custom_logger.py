"""
    Module for unit testing the customLogger class.

    Author: Isabela Yabe

    Last Modified: 06/11/2024

    Dependecies: 
        - unittest
        - os
        - sys
        - logging
        - CustomLogger   
"""

import logging
import unittest

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), 'src')))
from custom_logger import CustomLogger

class TestCustomLogger(unittest.TestCase):

    @classmethod
    def setUp(cls):
        cls.log_file = "test_app.log"

        cls.logger = CustomLogger(log_file=cls.log_file, level=logging.DEBUG).get_logger()

    def test_log_file_created_and_cleared(self):
        """
        Test if the log file is created and cleared at init.
        """
        self.assertTrue(os.path.exists(self.log_file))

        with open(self.log_file, "r") as file:
            content = file.read()
            self.assertEqual(content, "")
    
    def test_logging_to_file_and_console(self):
        """
        Test if the messages are saved on the log file and displayed on the console.
        """
        self.logger.debug("Debug message.")
        self.logger.info("Informational message.")
        self.logger.error("Error message.")

        with open(self.log_file, "r") as file:
            content = file.read()
            self.assertIn("Informational message", content)
            self.assertIn("Error message", content)
            self.assertNotIn("Debug message.", content)

    def test_password_filter(self):
        """
        Test if messages starting with 'password' are filtered out.
        """
        self.logger.info("Password message.")
        self.logger.info("Not password message.")

        with open(self.log_file, "r") as file:
            content = file.read()
            self.assertIn("Not password message.", content)
            self.assertNotIn("Password message.", content) 

    @classmethod
    def tearDownClass(cls):
        """
        Remove the log file after all test.
        """
        for handler in cls.logger.handlers:
            handler.close()
            cls.logger.removeHandler(handler)
        
        if os.path.exists(cls.log_file):
            os.remove(cls.log_file)
    
if __name__ == "__main__":
    unittest.main()
