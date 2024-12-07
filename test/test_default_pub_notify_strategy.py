"""
Module for Testing DefaultPubNotifyStrategy.

This module provides a suite of unit tests for the `DefaultPubNotifyStrategy` class using the `unittest` framework.
It tests the behavior of the notification strategy when notifying multiple subscribers, handling both success
and failure scenarios.

Author: Isabela Yabe
Last Modified: 07/12/2024
Status: Complete

Dependencies:
    - unittest
    - unittest.mock
    - custom_logger.setup_logger
    - pub_strategy.pub_notify_strategy.DefaultPubNotifyStrategy
"""
import unittest
from unittest.mock import MagicMock, patch
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), 'src')))
from pub_strategy.pub_notify_strategy import DefaultPubNotifyStrategy
from custom_logger import setup_logger

logger = setup_logger()

class MockSubscriber:
    """
    MockSubscriber class.

    This class is a mock implementation of a subscriber for testing purposes.
    """
    def __init__(self, table_name):
        """
        Initializes a mock subscriber.

        Parameters:
            table_name (str): The name of the table associated with the subscriber.
        """
        self.table_name = table_name

    def update(self, event_type, **data):
        """
        Mock update method to simulate subscriber behavior.

        Parameters:
            event_type (str): The type of the event.
            data (dict): The data associated with the event.
        """
        pass

class TestDefaultPubNotifyStrategy(unittest.TestCase):
    """
    TestDefaultPubNotifyStrategy class.

    This class provides unit tests for the `DefaultPubNotifyStrategy` class, focusing on its ability to notify
    multiple subscribers and handle edge cases.
    """
    def setUp(self):
        """
        Set up the test environment by creating a new instance of the DefaultPubNotifyStrategy and two mock subscribers.
        """
        self.strategy = DefaultPubNotifyStrategy()
        self.mock_subscriber_1 = MockSubscriber("Table1")
        self.mock_subscriber_2 = MockSubscriber("Table2")

        self.mock_subscriber_1.update = MagicMock()
        self.mock_subscriber_2.update = MagicMock()

    def test_notify_success(self):
        """
        Test notifying multiple subscribers successfully.
        """
        event_type = "TestEvent"
        data = {"key": "value"}
        subscribers = [self.mock_subscriber_1, self.mock_subscriber_2]

        self.strategy.notify(event_type, data, subscribers)

        self.mock_subscriber_1.update.assert_called_once_with(event_type, **data)
        self.mock_subscriber_2.update.assert_called_once_with(event_type, **data)
        logger.info("Test notify_success passed: OK!!! ---------------------------> TEST 1 OK!!!")

    def test_notify_failure(self):
        """
        Test handling failure when notifying a subscriber.
        """
        event_type = "TestEvent"
        data = {"key": "value"}
        subscribers = [self.mock_subscriber_1, self.mock_subscriber_2]

        self.mock_subscriber_1.update.side_effect = Exception("Update failed for Table1")

        self.strategy.notify(event_type, data, subscribers)

        self.mock_subscriber_1.update.assert_called_once_with(event_type, **data)
        self.mock_subscriber_2.update.assert_called_once_with(event_type, **data)
        logger.info("Test notify_failure passed: OK!!! ---------------------------> TEST 2 OK!!!")

if __name__ == "__main__":
    unittest.main()