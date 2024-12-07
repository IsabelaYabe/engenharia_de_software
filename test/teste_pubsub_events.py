import unittest
from unittest.mock import MagicMock, patch
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), 'src')))
from pub_strategy.pub_notify_strategy import DefaultPubNotifyStrategy
from sub_strategy.sub_update_strategy import DefaultSubUpdateStrategy, PurchaseProductSubUpdateStrategy
from event_manager.event_manager import EventManager
from custom_logger import setup_logger

logger = setup_logger()

class MockSubscriber:
    def __init__(self, table_name):
        self.table_name = table_name

    def update(self, event_type, **data):
        pass

class TestEventManager(unittest.TestCase):
    def setUp(self):
        self.event_manager = EventManager()
        self.mock_subscriber = MockSubscriber("mock_table")
    
    def test_subscribe_and_unsubscribe(self):
        self.event_manager.subscribe("TestEvent", self.mock_subscriber)
        self.assertIn(self.mock_subscriber, self.event_manager.subscribers["TestEvent"])
        
        self.event_manager.unsubscribe("TestEvent", self.mock_subscriber)
        self.assertNotIn(self.mock_subscriber, self.event_manager.subscribers["TestEvent"])
        logger.debug("Test subscribe and unsubscribe passed: OK!!! ---------------------------> TEST 1 OK!!!")

    def test_notify_with_default_strategy(self):
        self.mock_subscriber.update = MagicMock()
        self.event_manager.subscribe("TestEvent", self.mock_subscriber)

        event_data = {"key": "value"}
        self.event_manager.notify("TestEvent", event_data)

        self.mock_subscriber.update.assert_called_once_with("TestEvent", **event_data)
        logger.debug("Test notify with default strategy passed: OK!!! ---------------------------> TEST 2 OK!!!")

    def test_notify_with_custom_strategy(self):
        mock_strategy = MagicMock(spec=DefaultPubNotifyStrategy)
        self.event_manager.notify_strategies["CustomEvent"] = mock_strategy

        self.event_manager.subscribe("CustomEvent", self.mock_subscriber)
        event_data = {"key": "value"}
        self.event_manager.notify("CustomEvent", event_data)

        mock_strategy.notify.assert_called_once_with("CustomEvent", event_data, [self.mock_subscriber])
        logger.debug("Test notify with custom strategy passed: OK!!! ---------------------------> TEST 3 OK!!!")   

if __name__ == "__main__":
    unittest.main()
