import unittest
from unittest.mock import MagicMock, patch
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "src")))
from database_manager import DatabaseManager, Config, ConfigPub, ConfigSub
from event_manager.event_manager import EventManager
from custom_logger import setup_logger

logger = setup_logger()

class TestPubSubDecorator(unittest.TestCase):
    """
    Test suite for the pubsub decorator applied to the DatabaseManager class.
    """

    def setUp(self):
        """
        Sets up the test environment before each test case.

        Creates mock configurations and an instance of DatabaseManager with publish/subscribe capabilities.
        """
        self.mock_event_manager = MagicMock(spec=EventManager)
        self.mock_event_manager.notify = MagicMock()
        self.mock_event_manager.subscribers = MagicMock()

        config = Config(
            host="localhost",
            user="root",
            password="password",
            database="test_db",
            table_name="test_table",
            columns=["id", "name", "value"],
        )

        config_pub = ConfigPub(
            event_manager=self.mock_event_manager,
            events_type_pub=["event_create", "event_delete"]
        )

        config_sub = ConfigSub(
            event_manager=self.mock_event_manager,
            events_type_sub=["event_update"]
        )

        self.db_manager = DatabaseManager(config, config_pub=config_pub, config_sub=config_sub)

    def test_publish_event_success(self):
        """
        Tests the successful publishing of an event.
        Ensures that the notify method of the event manager is called with correct arguments.
        """
        event_type = "event_create"
        data = {"id": "123", "name": "test", "value": 42}

        self.db_manager._DatabaseManager__publish_event(event_type, **data)

        self.mock_event_manager.notify.assert_called_once_with(event_type, data)
        logger.info("Test publish event success: OK!!! ---------------------------> TEST 1 OK!!!")

    def test_publish_event_invalid_type(self):
        """
        Tests publishing an event with an invalid event type.
        Ensures that the event manager's `notify` method is not called.
        """
        event_type = "invalid_event"
        data = {"id": "123", "name": "test", "value": 42}

        with self.assertLogs("custom_logger", level="WARNING") as log:
            self.db_manager._DatabaseManager__publish_event(event_type, **data)
        
        self.assertIn("Event invalid_event is not in the configured publish list", log.output[0])
        self.mock_event_manager.notify.assert_not_called()
        logger.info("Test publish event invalid type: OK!!! ---------------------------> TEST 2 OK!!!")

    def test_subscribe_to_events(self):
        """
        Tests the subscription to events upon initialization.
        Ensures that the `subscribe` method of the event manager is called for each subscribed event.
        """
        self.mock_event_manager.subscribe.assert_any_call("event_update", self.db_manager)
        logger.info("Test subscribe to events: OK!!! ---------------------------> TEST 3 OK!!!")

    @patch("sub_strategy.default_sub_update_strategy.DefaultSubUpdateStrategy.update")
    def test_handle_subscribed_event(self, mock_strategy_update):
        """
        Tests handling a subscribed event.
        Ensures that the appropriate strategy's `update` method is called with correct data.
        """
        event_type = "event_update"
        data = {"id": "123", "name": "updated_name", "value": 84}

        self.db_manager.update(event_type, **data)

        mock_strategy_update.assert_called_once_with(data)
        logger.info("Test handle subscribed event: OK!!! ---------------------------> TEST 4 OK!!!")

    def test_handle_unsubscribed_event(self):
        """
        Tests handling an event that the class is not subscribed to.
        Ensures that no strategy is executed for the unsubscribed event.
        """
        event_type = "event_unsubscribed"
        data = {"id": "123"}

        with self.assertLogs("custom_logger", level="WARNING") as log:
            self.db_manager.update(event_type, **data)
        
        self.assertIn("Event event_unsubscribed is not in the configured subscribe list", log.output[0])
        logger.info("Test handle unsubscribed event: OK!!! ---------------------------> TEST 5 OK!!!")

    def test_subscribe_to_invalid_event(self):
        """
        Tests subscribing to an invalid event type.
        Ensures that a log warning is raised when the subscription fails.
        """
        self.mock_event_manager.subscribe.side_effect = Exception("Subscription failed")

        with self.assertLogs("custom_logger", level="ERROR") as log:
            DatabaseManager(
                Config(
                    host="localhost",
                    user="root",
                    password="password",
                    database="test_db",
                    table_name="test_table",
                    columns=["id", "name", "value"]
                ),
                config_pub=ConfigPub(event_manager=self.mock_event_manager, events_type_pub=["event_create"]),
                config_sub=ConfigSub(event_manager=self.mock_event_manager, events_type_sub=["event_invalid"])
            )
        
        self.assertIn("Failed to subscribe to event ['event_invalid']", log.output[0])
        logger.info("Test subscribe to invalid event: OK!!! ---------------------------> TEST 6 OK!!!")

if __name__ == "__main__":
    unittest.main()